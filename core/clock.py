import datetime
from core.errors import ParkomatIncorrectTimeException
from core import MoneyUnit

class Clock:

    def __init__(self):
        self._curr_time = datetime.now

    @property
    def curr_time(self):
        return self._curr_time

    @curr_time.setter
    def curr_time(self, new_time: str):
        try:
            self._curr_time = datetime.datetime(new_time)
        except ValueError:
            raise ParkomatIncorrectTimeException

