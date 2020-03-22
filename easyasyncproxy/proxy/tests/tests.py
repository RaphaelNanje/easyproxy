import unittest
from unittest import IsolatedAsyncioTestCase

import requests

from easyasyncproxy.proxy import ProxyApi

url = 'http://httpbin.org/ip'

api = ProxyApi()


class TestAsyncProxyApi(IsolatedAsyncioTestCase):

    async def test_get(self):
        loop = self._asyncioTestLoop
        print('TestAsyncProxyApi.test_get',
              'looping until we get a valid working proxy')
        while True:
            try:
                result = await api.get(url, loop=loop)
            except Exception as e:
                continue
            else:
                ip = requests.get(url).json().get('origin')
                response = result.response
                self.assertEqual(response.status_code, 200)
                self.assertTrue('origin' in response.json())
                self.assertNotEqual(ip, response.json().get('origin'))
                break

    async def test_post(self):
        loop = self._asyncioTestLoop
        post_url = 'https://eap-tests.free.beeceptor.com'
        print('TestAsyncProxyApi.test_post',
              'looping until we get a valid working proxy')
        while True:
            try:
                result = await api.post(post_url, loop=loop, data=dict(
                    title='some title',
                    body='some body'
                ))
            except Exception as e:
                continue
            else:
                await api.manager.release(result.proxy)
                self.assertEqual(result.response.json(),
                                 dict(content='Great!'))
                break


if __name__ == '__main__':
    unittest.main()
