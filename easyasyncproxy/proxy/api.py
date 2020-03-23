import asyncio
import functools
from typing import Iterable, Union, TYPE_CHECKING, Optional

import attr
import requests
from requests import Response, Session
from yarl import URL

from easyasyncproxy.proxy import config
from easyasyncproxy.proxy.exceptions import BadProxyError, bad_proxy_exceptions

if TYPE_CHECKING:
    from easyasyncproxy.proxy import Proxy


class ProxyApi:

    def __init__(self, links=None, proxies: Iterable[tuple] = None,
                 timeout=5, headers: dict = None, clear_on_fail=False) -> None:
        """

        Args:
            links:
            proxies:
            timeout:
            headers:
            clear_on_fail: Whether to clear proxies from session when a
                BadProxy is raised (default: True)
        """
        self.headers = headers or config.HEADERS
        self.timeout = timeout

        self._loop = asyncio.get_event_loop()

        from easyasyncproxy.proxy import AsyncProxyManager
        self.manager = AsyncProxyManager(from_file=proxies, links=links or [])
        self.clear_on_fail = True

    async def get(self, url: Union[str, URL], params: dict = None, loop=None,
                  headers: dict = None, timeout: int = None, **kwargs):
        proxy = await self.manager.acquire()
        loop = loop or self._loop
        future = loop.run_in_executor(None, functools.partial(
            requests.get,
            url,
            params=params or {},
            timeout=timeout or self.timeout,
            headers=headers or self.headers,
            proxies=proxy.as_dict,
            **kwargs
        ))
        return ProxyResponseResult(proxy, await future)

    async def post(self, url: Union[str, URL], data: dict = None, loop=None,
                   headers: dict = None, timeout: int = None, **kwargs):
        proxy = await self.manager.acquire()
        loop = loop or self._loop
        future = loop.run_in_executor(None, functools.partial(
            requests.post,
            url,
            data=data or {},
            timeout=timeout or self.timeout,
            headers=headers or self.headers,
            proxies=proxy.as_dict,
            **kwargs
        ))
        return ProxyResponseResult(proxy, await future)

    async def session_post(self, session: Session, url: Union[str, URL],
                           data: dict = None, loop=None, timeout: int = None,
                           **kwargs):
        proxy = self.get_proxy_from_session(session)
        if not any(session.proxies):
            proxy = await self.manager.acquire()
            session.proxies.update(proxy)
        loop = loop or self._loop
        future = loop.run_in_executor(None, functools.partial(
            session.post,
            url,
            data=data,
            timeout=timeout or self.timeout,
            **kwargs
        ))
        try:
            response = await future
        except bad_proxy_exceptions as e:
            if self.clear_on_fail:
                session.proxies.clear()
            raise BadProxyError(proxy, str(e))
        return ProxyResponseResult(proxy, response)

    async def session_get(self, session: Session, url: Union[str, URL],
                          params: dict = None, loop=None, timeout: int = None,
                          **kwargs):
        loop = loop or self._loop
        proxy = self.get_proxy_from_session(session)
        if not proxy:
            proxy = await self.manager.acquire()
            session.proxies.update(proxy.as_dict)
        future = loop.run_in_executor(None, functools.partial(
            session.get,
            url,
            params=params,
            timeout=timeout or self.timeout,
            **kwargs
        ))
        try:
            response = await future
        except bad_proxy_exceptions as e:
            if self.clear_on_fail:
                session.proxies.clear()
            raise BadProxyError(proxy, str(e))
        return ProxyResponseResult(proxy, response)

    @staticmethod
    def get_proxy_from_session(session: Session) -> Optional['Proxy']:
        proxy_dict = session.proxies.copy()
        if not any(proxy_dict):
            return None
        protocol, link = proxy_dict.popitem()
        from easyasyncproxy.proxy import Proxy
        return Proxy.from_url(link)


@attr.s(auto_attribs=True)
class ProxyResponseResult:
    proxy: 'Proxy'
    response: Response
