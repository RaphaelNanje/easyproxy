import requests

from easyasyncproxy.scraperapi.utilities import logger


class ScraperKey:
    code: str = ''
    uses: int = 0
    max_uses: int
    concurrent_limit: int

    def __init__(self, code: str) -> None:
        self.code = code
        self.enabled = True
        self.get_usage()

    def get_usage(self):
        r = requests.get(
                f'http://api.scraperapi.com/account?api_key={self.code}'
        )
        if not r:
            self.disable()
            return
        json = r.json()
        count_ = json['requestCount']
        limit_ = json['requestLimit']
        concurrency_limit_ = json['concurrencyLimit']
        self.uses = int(count_)
        self.max_uses = int(limit_)
        self.concurrent_limit = int(concurrency_limit_)
        logger.info('Scraper Key "%s..." uses left: %s' % (
                self.code[:8], self.uses_left))
        if self.uses >= self.max_uses:
            self.disable()

    def disable(self):
        self.enabled = False
        logger.info('disabling key: "%s..."', self.code[:8])

    @property
    def uses_left(self):
        return self.max_uses - self.uses

    def inc(self):
        self.uses += 1

    def __str__(self):
        return f'{self.code[:8]}...'

    def __repr__(self):
        return f'{self.code[:8]}...'
