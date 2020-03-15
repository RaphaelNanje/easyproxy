import asyncio
import os
import unittest
from typing import Coroutine

import requests
from dotenv import load_dotenv
from requests import Response

from easyproxy.scraperapi.api import ScraperApi

load_dotenv()

url = 'http://httpbin.org/ip'


def load_keys():
    keys = os.getenv('SCRAPER_API_KEYS').strip()
    keys = keys.split(',')
    return [k for k in keys if k]


keys = load_keys()

api = ScraperApi(keys=keys)


class TestAsyncScraperApi(unittest.TestCase):

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

    def test_get(self):
        result: Response = self.do_run(api.get(url))

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
