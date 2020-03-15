import asyncio
import functools
from typing import Union, Iterable

import requests
from requests import Response
from yarl import URL

from easyproxy.scraperapi import config
from easyproxy.scraperapi.scraperkey import ScraperKey
from easyproxy.scraperapi.manager import ScraperApiManager
from easyproxy.scraperapi.utilities import UseCount


class ScraperApi:

    def __init__(self, headers=config.HEADERS, timeout=5,
                 keys: Iterable = None) -> None:
        self.headers = headers
        self.timeout = timeout
        self._loop = asyncio.get_event_loop()
        self.total_uses = UseCount(0)

        valid_keys = self.get_valid_keys(keys)
        self.manager = ScraperApiManager(valid_keys)

    async def get(self, url: Union[str, URL], **kwargs):
        key = await self.manager.acquire()
        future = self._loop.run_in_executor(None, functools.partial(
                requests.get,
                config.SCRAPER_API_BASE_URL,
                params=self._generate_params(url, key),
                timeout=self.timeout,
                headers=self.headers,
                **kwargs
        ))
        response: Response = await future
        if response.status_code == 200:
            self.total_uses += 1
        return response

    @staticmethod
    def _generate_params(url, key: ScraperKey):
        p = config.params.copy()
        p['url'] = url
        p['api_key'] = key.code
        payload_ = ''
        for k, v in p.items():
            payload_ += f'{k}={v}&'
        payload_ = payload_.strip('&')
        return payload_

    @staticmethod
    def get_valid_keys(keys):
        valid_keys = []
        for code in keys:
            key = ScraperKey(code)
            if key.enabled:
                valid_keys.append(key)
        return valid_keys
