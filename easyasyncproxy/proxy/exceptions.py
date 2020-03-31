import socket
from typing import TYPE_CHECKING

import requests.exceptions
import urllib3.exceptions

if TYPE_CHECKING:
    from easyasyncproxy.proxy import Proxy


class BadProxyError(Exception):
    def __init__(self, proxy: 'Proxy', *args: object) -> None:
        super().__init__(*args)
        self.proxy = proxy


bad_proxy_exceptions = (
    requests.exceptions.ProxyError,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ReadTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.ChunkedEncodingError,
    urllib3.exceptions.ReadTimeoutError,
    urllib3.exceptions.MaxRetryError,
    urllib3.exceptions.ConnectTimeoutError,
    socket.timeout,
)
