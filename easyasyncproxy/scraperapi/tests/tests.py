import os
import unittest
from unittest import IsolatedAsyncioTestCase

import requests
from dotenv import load_dotenv

from easyasyncproxy.scraperapi.api import ScraperApi

load_dotenv()

url = 'http://httpbin.org/ip'


def load_keys():
    keys = os.getenv('SCRAPER_API_KEYS').strip()
    keys = keys.split(',')
    return [k for k in keys if k]


keys = load_keys()

api = ScraperApi(keys=keys)


class TestScraperApi(IsolatedAsyncioTestCase):

    async def test_get(self):
        loop = self._asyncioTestLoop
        result = await api.get(url, loop=loop)
        ip = requests.get(url).json().get('origin')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('origin' in result.json())
        self.assertNotEqual(ip, result.json().get('origin'))


if __name__ == '__main__':
    unittest.main()
