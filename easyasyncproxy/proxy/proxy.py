import attr


@attr.s(auto_attribs=True)
class Proxy:
    host: str
    port: str
    bad = False

    def set_bad(self):
        self.bad = True

    @property
    def as_dict(self):
        return dict(https=self.https_formatted,
                    http=self.http_formatted)

    @property
    def https_formatted(self):
        return 'https://%s:%s' % (self.host, self.port)

    @property
    def http_formatted(self):
        return 'http://%s:%s' % (self.host, self.port)

    def __str__(self) -> str:
        return str(self.as_dict)
