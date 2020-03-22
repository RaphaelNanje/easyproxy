import asyncio
import functools
from typing import Iterable, Union

import attr
import requests
from requests import Response
from yarl import URL

from easyasyncproxy.proxy import config


class ProxyApi:

    def __init__(self, links=None, proxies: Iterable[tuple] = None,
                 timeout=5, headers: dict = None) -> None:
        self.headers = headers or config.HEADERS
        self.timeout = timeout

        self._loop = asyncio.get_event_loop()

        from easyasyncproxy.proxy import AsyncProxyManager
        self.manager = AsyncProxyManager(from_file=proxies, links=links or [])

    async def get(self, url: Union[str, URL], params: dict = None, loop=None,
                  headers: dict = None, timeout: int = None,
                  **kwargs):
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


@attr.s(auto_attribs=True)
class ProxyResponseResult:
    proxy: str
    response: Response
