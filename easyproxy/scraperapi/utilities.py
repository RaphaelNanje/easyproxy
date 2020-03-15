import logging


class UseCount(int):
    def inc(self):
        self.__add__(1)


logger = logging.getLogger(__name__)