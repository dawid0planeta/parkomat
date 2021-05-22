from datetime import datetime, date, time, timedelta
from parkomat.core.errors import ParkomatIncorrectTimeException

class Clock:
    '''
    Implements a internal clock for Parkomat
    '''

    def __init__(self):
        self._curr_time = datetime.now()

    def add_times(self, curr: datetime, delta: timedelta) -> datetime:
        '''
        Calculates the proper leave time given current time and time that the user paid for
        :param curr: current time
        :param delta: time that the user paid for
        :return: leave time
        '''
        # check if today is weekend
        while curr.weekday() in (5, 6):
            curr = self._get_start_next_day(curr)

        # if time fits today just return the added time
        today_20 = datetime.combine(curr.date(), time(20))
        time_left_in_day = (today_20 - self.curr_time)
        if delta <= time_left_in_day:
            return curr + delta

        delta -= time_left_in_day
        # go trough as many days as you can given delta
        curr = self._get_start_next_day(curr)
        day = timedelta(minutes=720)
        while delta >= day:
            delta -= day
            curr = self._get_start_next_day(curr)

        return curr + delta

    def _get_start_next_day(self, curr) -> datetime:
        '''
        Given current time, returns start of the next paying day
        :param curr: current time
        :return: start of next paying day
        '''
        new_date = datetime.combine(curr.date() + timedelta(days=1), time(hour=8))
        if new_date.weekday() in (5, 6):
            return self._get_start_next_day(new_date)
        return new_date

    def update_time(self) -> None:
        """
        Used to incerement the clock
        """
        self._curr_time = self._curr_time + timedelta(seconds=1)

    @property
    def curr_time(self) -> datetime:
        return self._curr_time

    @curr_time.setter
    def curr_time(self, new_time: str):
        """
        Sets current time to arbitrary hour on the same day, given that it's correct
        :param new_time: new time in ISO format
        """
        try:
            self._curr_time = datetime.combine(self._curr_time.date(), time.fromisoformat(new_time))
        except ValueError:
            raise ParkomatIncorrectTimeException

