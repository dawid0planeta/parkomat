from decimal import Decimal
from typing import Tuple
from datetime import datetime, timedelta
from parkomat.core.errors import *
from parkomat.core.clock import Clock
from parkomat.core.money_storage import MoneyStorage
from parkomat.core.money_unit import MoneyUnit

class Parkomat:
    """
    Implements the main Parkomat class responsible for all the external
    """

    _allowed = {'0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00', '10.00', '20.00', '50.00'}

    def __init__(self):
        self._clock = Clock()
        self._money_storage = MoneyStorage(self._allowed, [])
        self._leave_time = self.curr_time
        self._current_delta = timedelta(seconds=0)
        self._money_put = []
        self._registration_number = ''

    def buy(self) -> Tuple[str, datetime, datetime]:
        """
        Checks the details of a transaction and finalises it.
        :return: Tuple of registration number, current time, and leave time
        """
        self._update_delta_based_on_money()
        self._update_leave_time()
        if self._registration_number == '':
            raise ParkomatEmptyRegistrationNumberException

        if len(self._money_put) == 0:
            raise ParkomatNoMoneyInsertedException

        if not all(c.isdigit() or c.isupper() for c in self._registration_number):
            raise ParkomatIncorrectRegistrationNumberException


        receipt = (self._registration_number, self.curr_time, self._leave_time)
        self.reset()
        return receipt

    def put_money(self, money: MoneyUnit) -> None:
        """
        Puts money unit into storage and updates all neccessary variables accordingly
        :param money: money unit to be added
        """
        self._money_storage.put_money(money)
        self._money_put.append(money)
        self._update_delta_based_on_money()
        self._update_leave_time()

    def reset(self) -> None:
        """
        Resets the Parkomat instance to starting state for new transaction
        """
        self._leave_time = self.curr_time
        self._current_delta = timedelta(seconds=0)
        for each in self._money_put:
            self._money_storage.remove_money(each)
        self._money_put = []
        self._registration_number = ''

    def _update_leave_time(self) -> None:
        """
        Calculates and updates leave time based on current time and time the user paid for
        """
        self._leave_time = self._clock.add_times(self.curr_time, self._current_delta)

    def _update_delta_based_on_money(self) -> None:
        """
        Calculates the proper amount of time the user paid for
        """

        total_value = sum([unit.value for unit in self._money_put])

        # first hour
        if total_value <= Decimal('2'):
            self._current_delta = timedelta(seconds=float(total_value/Decimal('2')*3600))
            return

        total_value -= Decimal('2')
        self._current_delta = timedelta(seconds=3600)

        # second hour
        if total_value <= Decimal('4'):
            self._current_delta += timedelta(seconds=float(total_value/Decimal('4')*3600))
            return

        total_value -= Decimal('4')
        self._current_delta += timedelta(seconds=3600)

        # rest of the time
        self._current_delta += timedelta(seconds=float(total_value/Decimal('5')*3600))

    @property
    def leave_time(self) -> datetime:
        self._update_leave_time()
        return self._leave_time

    @property
    def curr_time(self) -> datetime:
        return self._clock.curr_time

    @curr_time.setter
    def curr_time(self, new_time: datetime) -> None:
        self._clock.curr_time = new_time

    def update_time(self) -> None:
        self._clock.update_time()

    @property
    def registration_number(self) -> str:
        return self._registration_number

    @registration_number.setter
    def registration_number(self, new_number: str) -> None:
        self._registration_number = new_number

