from core.errors import ParkomatIncorrectRegistrationNumber
from decimal import Decimal
from typing import Tuple
from errors import ParkomatFullException
from clock import Clock
from money_storage import MoneyStorage
from money_unit import MoneyUnit
from datetime import datetime, timedelta, date, time

class Parkomat:

    _allowed = {'0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00', '10.00', '20.00', '50.00'}

    def __init__(self):
        self._clock = Clock()
        self._money_storage = MoneyStorage(self._allowed, [])
        self._leave_time = self.curr_time
        self._current_delta = timedelta(seconds=0)
        self._money_put = []
        self._registration_number = ''

    def buy(self) -> Tuple[str, datetime, datetime]:
        self._update_delta_based_on_money()
        self._update_leave_time()

        receipt = (self._registration_number, self.curr_time, self._leave_time)
        self._reset()
        return receipt

    def put_money(self, money: MoneyUnit) -> None:
        self._money_storage.put_money(money)
        self._money_put.append(money)
        self._update_delta_based_on_money()
        self._update_leave_time()

    def _reset(self) -> None:
        self._leave_time = self.curr_time
        self._current_delta = timedelta(seconds=0)
        self._money_put = []
        self._registration_number = ''

    def _update_leave_time(self) -> None:
        self._leave_time = self._clock.add_times(self.curr_time, self._current_delta)

    def _update_delta_based_on_money(self) -> None:
        total_value = sum([unit.value for unit in self._money_put])
        if total_value <= Decimal('2'):
            self._current_delta = timedelta(seconds=float(total_value/Decimal('2')*3600))
            return

        total_value -= Decimal('2')
        self._current_delta = timedelta(seconds=3600)

        if total_value <= Decimal('4'):
            self._current_delta += timedelta(seconds=float(total_value/Decimal('4')*3600))
            return

        total_value -= Decimal('4')
        self._current_delta += timedelta(seconds=3600)

        self._current_delta += timedelta(seconds=float(total_value/Decimal('5')*3600))

    @property
    def leave_time(self) -> datetime:
        return self._leave_time

    @property
    def curr_time(self) -> datetime:
        return self._clock.curr_time

    @property
    def registration_number(self):
        return self._registration_number

    @property.setter
    def registration_number(self, new_number: str):
        if all(c.isdigit() or c.isupper() for c in new_number):
            self._registration_number = new_number
        else:
            raise ParkomatIncorrectRegistrationNumber

