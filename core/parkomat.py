from core.clock import Clock
from core.money_storage import MoneyStorage
from core.money_unit import MoneyUnit
from datetime import datetime, timedelta, date, time

class Parkomat:

    _allowed = ('0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00', '10.00', '20.00', '50.00')

    def __init__(self):
        self._clock = Clock()
        self._money_storage = MoneyStorage(self._allowed, [])
        self._leave_time = self.curr_time
        self._current_delta = timedelta(minutes=0)


    def update_delta(self, delta: timedelta) -> None:
        self._current_delta = self._current_delta + delta
        self._update_leave_time()

    def _update_leave_time(self) -> None:
        self._leave_time = Clock.add_times(self.curr_time, self._current_delta)


    @property
    def leave_time(self) -> datetime:
        return self._leave_time

    @property
    def curr_time(self) -> datetime:
        return self._clock.curr_time
