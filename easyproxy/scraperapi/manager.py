import asyncio
from asyncio import Queue, CancelledError
from collections import UserList
from time import time
from typing import Iterable as Iterable, List

from easyproxy.scraperapi.scraperkey import ScraperKey
from easyproxy.scraperapi.utilities import logger


class ScraperApiManager(UserList):

    def __init__(self, init: Iterable[ScraperKey]) -> None:
        super().__init__(init)
        self.queue = Queue()

        for key in self.valid_keys:
            for _ in range(key.concurrent_limit):
                self.queue.put_nowait(key)
        logger.info('Refreshing scraper api key usages...')

    async def acquire(self) -> ScraperKey:
        logger.debug('a worker is attempting to acquire a key...')
        t1 = time()
        try:
            key = await asyncio.wait_for(self.queue.get(), timeout=120)
        except CancelledError:
            pass
        except TimeoutError:
            logger.exception('Timed out while waiting for a key')
            raise
        else:
            logger.debug('key %s was acquired after waiting for %.2f seconds',
                         key.code[:8], time() - t1)
            return key

    async def release(self, key: ScraperKey):
        if key.enabled:
            await self.queue.put(key)
        logger.debug('Key %s was released', key)

    def get_stats(self):
        req_left = sum(list(map(lambda key: key.uses_left, self.valid_keys)))
        stats = dict(
                valid_scraper_keys=len(self.valid_keys),
                key_requests_left=req_left
        )
        return stats

    def ran_out(self):
        raise NoMoreKeysError('Ran out of usable keys')

    @property
    def valid_keys(self) -> List[ScraperKey]:
        valid_keys = list(
                filter(lambda key: key.enabled and key.uses < key.max_uses,
                       self))
        if not any(valid_keys):
            self.ran_out()
        return valid_keys


class NoMoreKeysError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
