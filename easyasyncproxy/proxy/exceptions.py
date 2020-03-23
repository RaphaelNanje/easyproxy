import socket
from typing import TYPE_CHECKING

import requests
from requests import ConnectTimeout, ReadTimeout
from requests.exceptions import ProxyError, ChunkedEncodingError
from urllib3.exceptions import (ConnectTimeoutError, ReadTimeoutError,
                                MaxRetryError)

if TYPE_CHECKING:
    from easyasyncproxy.proxy import Proxy


class BadProxyError(Exception):
    def __init__(self, proxy: 'Proxy', *args: object) -> None:
        super().__init__(*args)
        self.proxy = proxy


bad_proxy_exceptions = (ConnectTimeoutError, ProxyError, ConnectTimeout,
                        ReadTimeoutError, ReadTimeout, socket.timeout,
                        requests.ConnectionError, MaxRetryError,
                        ChunkedEncodingError)
