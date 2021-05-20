import datetime
from datetime import datetime, date, time, timedelta
from core.errors import ParkomatIncorrectTimeException
from core import MoneyUnit

class Clock:

    def __init__(self):
        self._curr_time = datetime.now()

    @classmethod
    def add_times(cls, curr: datetime, delta_in_minutes: int) -> datetime:
        today_20 = datetime.combine(date.today(), time(20))
        minutes_left_in_day = Clock.timedelta_to_minutes(today_20 - datetime.now())
        if delta_in_minutes <= minutes_left_in_day:
            return curr + timedelta(minutes=delta_in_minutes)

        delta_in_minutes -= minutes_left_in_day
        curr = cls._get_start_next_day(curr)
        while delta_in_minutes >= 720:
            delta_in_minutes -= 720
            curr = cls._get_start_next_day(curr)

        return curr + timedelta(minutes=delta_in_minutes)


    @classmethod
    def _get_start_next_day(cls, curr) -> datetime:
        new_date = datetime.combine(curr.date() + timedelta(days=1), time(hour=8, seconds=curr.second))
        if new_date.weekday() in (5, 6):
            return cls._get_start_next_day(new_date)
        return new_date

    @classmethod
    def _timedelta_to_minutes(cls, delta: timedelta) -> int:
        return int((delta.seconds/60) + 1)

    @property
    def curr_time(self) -> datetime:
        return self._curr_time

    @curr_time.setter
    def curr_time(self, new_time: str):
        try:
            self._curr_time = datetime.datetime(new_time)
        except ValueError:
            raise ParkomatIncorrectTimeException

