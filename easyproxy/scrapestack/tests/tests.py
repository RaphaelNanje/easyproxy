import asyncio
import os
import unittest
from typing import Coroutine

import requests
from dotenv import load_dotenv
from requests import Response

from easyproxy.scrapestack import ScrapeStackApi

url = 'http://httpbin.org/ip'
load_dotenv()

key = os.getenv('SCRAPE_STACK_KEY')


class TestAsyncScrapeStack(unittest.TestCase):

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.api = ScrapeStackApi(key)

    def test_get(self):
        result: Response = self.do_run(self.api.get(url))

        ip = requests.get(url).json().get('origin')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('origin' in result.json())
        self.assertNotEqual(ip, result.json().get('origin'))

    def do_run(self, future: Coroutine):
        return self.loop.run_until_complete(future)

    def tearDown(self) -> None:
        self.loop.close()


if __name__ == '__main__':
    unittest.main()
