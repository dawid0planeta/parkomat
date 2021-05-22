from datetime import datetime, date, time, timedelta
from parkomat.core.errors import ParkomatIncorrectTimeException

class Clock:

    def __init__(self):
        self._curr_time = datetime.combine(date(2021, 5, 24), datetime.now().time())
        self._curr_time = datetime.now()

    def add_times(self, curr: datetime, delta: timedelta) -> datetime:
        while curr.weekday() in (5, 6):
            curr = self._get_start_next_day(curr)

        today_20 = datetime.combine(curr.date(), time(20))
        time_left_in_day = (today_20 - self.curr_time)
        if delta <= time_left_in_day:
            return curr + delta

        delta -= time_left_in_day
        curr = self._get_start_next_day(curr)
        day = timedelta(minutes=720)
        while delta >= day:
            delta -= day
            curr = self._get_start_next_day(curr)

        return curr + delta

    def _get_start_next_day(self, curr) -> datetime:
        new_date = datetime.combine(curr.date() + timedelta(days=1), time(hour=8))
        if new_date.weekday() in (5, 6):
            return self._get_start_next_day(new_date)
        return new_date

    def update_time(self) -> None:
        self._curr_time = self._curr_time + timedelta(seconds=1)

    @property
    def curr_time(self) -> datetime:
        return self._curr_time

    @curr_time.setter
    def curr_time(self, new_time: str):
        try:
            self._curr_time = datetime.combine(self._curr_time.date(), time.fromisoformat(new_time))
        except ValueError:
            raise ParkomatIncorrectTimeException

