import asyncio
import functools
from typing import Union, Iterable

import attr
import requests
from requests import Response
from yarl import URL

from easyasyncproxy.scraperapi import config
from easyasyncproxy.scraperapi.manager import ScraperApiManager
from easyasyncproxy.scraperapi.scraperkey import ScraperKey
from easyasyncproxy.scraperapi.utilities import UseCount


class ScraperApi:
    """
    https://www.scraperapi.com/
    """

    def __init__(self, keys: Iterable[str], headers: dict = None,
                 timeout=5) -> None:
        """
        Args:
            keys: A list of keys to be used
            headers: Optional headers
            timeout: Default = 5
        """
        self.headers = headers or config.HEADERS
        self.timeout = timeout
        self._loop = asyncio.get_event_loop()
        self.total_uses = UseCount(0)

        valid_keys = self.get_valid_keys(keys)
        self.manager = ScraperApiManager(valid_keys)

    async def get(self, url: Union[str, URL], loop=None, **kwargs):
        """
        Make a get request using the ScraperApi service

        Args:
            url: The website to scrape
            loop: Optional loop parameter for testing
            **kwargs: Any additional arguments that will be passed to requests

        Returns: Response object

        """
        key = await self.manager.acquire()
        loop = loop or self._loop
        future = loop.run_in_executor(None, functools.partial(
            requests.get,
            config.SCRAPER_API_BASE_URL,
            params=self._generate_params(url, key),
            timeout=self.timeout,
            headers=self.headers,
            **kwargs
        ))
        response: Response = await future
        return ScraperApiResponse(key, response)

    @staticmethod
    def _generate_params(url: str, scraper_key: ScraperKey):
        """
        Create a string of parameters containing API information

        Args:
            url (str): The website to be retrieved.
            scraper_key (ScraperKey): An object containing a ScraperApi key.

        Returns: A string of parameters that should be added to the ScraperApi
        base url

        """
        parameters = config.params.copy()
        parameters['url'] = url
        parameters['api_key'] = scraper_key.code
        payload = ''
        for key, value in parameters.items():
            payload += f'{key}={value}&'
        payload = payload.strip('&')
        return payload

    @staticmethod
    def get_valid_keys(keys):
        valid_keys = []
        for code in keys:
            key = ScraperKey(code)
            if key.enabled:
                valid_keys.append(key)
        return valid_keys


@attr.s(auto_attribs=True)
class ScraperApiResponse:
    key: ScraperKey
    response: Response
