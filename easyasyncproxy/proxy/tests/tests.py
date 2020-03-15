import unittest
from unittest import IsolatedAsyncioTestCase

import requests
from requests.exceptions import ProxyError

from easyasyncproxy.proxy import ProxyApi

url = 'http://httpbin.org/ip'

api = ProxyApi()


class TestAsyncProxyApi(IsolatedAsyncioTestCase):

    async def test_get(self):
        try:
            loop = self._asyncioTestLoop
            result = await api.get(url, loop=loop)
        except ProxyError:
            print('Returned from acceptable ProxyError')
            return
        ip = requests.get(url).json().get('origin')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('origin' in result.json())
        self.assertNotEqual(ip, result.json().get('origin'))

if __name__ == '__main__':
    unittest.main()
