import asyncio
import unittest

import requests
from requests import Response
from requests.exceptions import ProxyError

from easyproxy import ProxyApi

url = 'http://httpbin.org/ip'

api = ProxyApi()


class TestAsyncProxyApi(unittest.TestCase):

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

    def test_get(self):
        try:
            result: Response = self.loop.run_until_complete(api.get(url))
        except ProxyError:
            print('Returned from acceptable ProxyError')
            return
        ip = requests.get(url).json().get('origin')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('origin' in result.json())
        self.assertNotEqual(ip, result.json().get('origin'))

    def tearDown(self) -> None:
        self.loop.close()


if __name__ == '__main__':
    unittest.main()
