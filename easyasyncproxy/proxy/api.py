import asyncio
import functools
from typing import Iterable, Union

import requests
from requests import Response
from yarl import URL

from easyasyncproxy.proxy import config, AsyncProxyManager


class ProxyApi:

    def __init__(self, links=None, proxies: Iterable[tuple] = None,
                 timeout=5, headers: dict = None) -> None:
        self.headers = headers or config.HEADERS
        self.timeout = timeout

        self._loop = asyncio.get_event_loop()
        self.manager = AsyncProxyManager(from_file=proxies, links=links or [])

    async def get(self, url: Union[str, URL], params: dict = None, loop=None,
                  **kwargs) -> Response:
        proxy = await self.manager.acquire()
        loop = loop or self._loop
        future = loop.run_in_executor(None, functools.partial(
            requests.get,
            url,
            params=params or {},
            timeout=self.timeout,
            headers=self.headers,
            proxies=proxy.as_dict,
            **kwargs
        ))
        return await future
