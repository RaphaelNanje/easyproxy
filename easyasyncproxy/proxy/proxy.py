from urllib.parse import urlsplit

import attr


@attr.s(auto_attribs=True)
class Proxy:
    host: str
    port: str
    username = ''
    password = ''
    bad = False

    def set_bad(self):
        self.bad = True

    @property
    def as_dict(self):
        return dict(https=self.https_formatted,
                    http=self.http_formatted)

    @property
    def socks5_as_dict(self):
        return dict(http=f'socks5://{self.host}:{self.port}',
                    https=f'socks5://{self.host}:{self.port}')

    @property
    def https_formatted(self):
        return 'https://%s:%s' % (self.host, self.port)

    @property
    def http_formatted(self):
        return 'http://%s:%s' % (self.host, self.port)

    def __str__(self) -> str:
        return str(self.as_dict)

    @classmethod
    def from_url(cls, url: str):
        split = urlsplit(url)
        return Proxy(split.hostname, str(split.port))
