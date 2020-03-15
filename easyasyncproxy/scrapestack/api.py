import asyncio
import functools
from typing import Union

import requests
from requests import Response
from yarl import URL

from easyasyncproxy.scrapestack import config


class ScrapeStackApi:

    def __init__(self, access_key: str,
                 headers: dict = None, timeout=5) -> None:
        self.headers = headers or config.HEADERS
        self.timeout = timeout
        self._access_key = access_key

        self._loop = asyncio.get_event_loop()

    async def get(self, url: Union[str, URL], loop=None,
                  **kwargs) -> Response:
        loop = loop or self._loop
        future = loop.run_in_executor(None, functools.partial(
            requests.get,
            config.SCRAPESTACK_BASE_URL,
            params=self._generate_params(url),
            timeout=self.timeout,
            headers=self.headers,
            **kwargs
        ))

        return await future

    def _generate_params(self, url) -> str:
        parameters = config.params.copy()
        parameters['url'] = url
        parameters['access_key'] = self._access_key
        payload_ = ''
        for key, value in parameters.items():
            payload_ += f'{key}={value}&'
        payload_ = payload_.strip('&')
        return parameters
