import os
import unittest
from unittest import IsolatedAsyncioTestCase

import requests
from dotenv import load_dotenv

from easyasyncproxy.scrapestack import ScrapeStackApi

url = 'http://httpbin.org/ip'
load_dotenv()

key = os.getenv('SCRAPE_STACK_KEY')


class TestScrapeStack(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.api = ScrapeStackApi(key)

    async def test_get(self):
        loop = self._asyncioTestLoop
        result = await self.api.get(url, loop=loop)

        ip = requests.get(url).json().get('origin')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('origin' in result.json())
        self.assertNotEqual(ip, result.json().get('origin'))


if __name__ == '__main__':
    unittest.main()
