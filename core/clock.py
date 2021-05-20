import datetime
from datetime import datetime, date, time, timedelta
from core.errors import ParkomatIncorrectTimeException
from core import MoneyUnit

class Clock:

    def __init__(self):
        self._curr_time = datetime.now()

    def add_times(self, curr: datetime, delta: timedelta) -> datetime:
        today_20 = datetime.combine(date.today(), time(20))
        time_left_in_day = (today_20 - self.curr_time)
        if delta <= time_left_in_day:
            return curr + delta

        delta -= time_left_in_day
        curr = self._get_start_next_day(curr)
        day = timedelta(minutes=720)
        while delta >= day:
            delta -= day
            curr = self._get_start_next_day(curr)
        return curr + day

    def _get_start_next_day(self, curr) -> datetime:
        new_date = datetime.combine(curr.date() + timedelta(days=1), time(hour=8))
        if new_date.weekday() in (5, 6):
            return self._get_start_next_day(new_date)
        return new_date

    @property
    def curr_time(self) -> datetime:
        return self._curr_time

    @curr_time.setter
    def curr_time(self, new_time: str):
        try:
            self._curr_time = datetime.datetime(new_time)
        except ValueError:
            raise ParkomatIncorrectTimeException

