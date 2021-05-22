from typing import List, Set, Dict

from parkomat.core.money_unit import MoneyUnit
from parkomat.core.errors import ParkomatFullException

class MoneyStorage:
    """
    Implements a money storage class with proper checks, and constraints
    """

    _coins = {'0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00'}

    def __init__(self, allowed_values: Set[str], initial_units: List[MoneyUnit]):
        self._money = {key: [] for key in allowed_values}
        for unit in initial_units:
            self._money[str(unit)].append(unit)

    def put_money(self, unit: MoneyUnit) -> None:
        """
        Adds a money unit to storage checking if there is space for it
        :param unit: money unit that is supposed to be added
        """
        str_unit = str(unit)
        if str_unit not in self._coins or len(self._money[str_unit]) < 200:
            self._money[str_unit].append(unit)
        else:
            raise ParkomatFullException

    def remove_money(self, unit: MoneyUnit) -> None:
        """
        Removes a money unit from storage. Used if user decides to cancel the transaction
        :param unit: money unit to be removed
        """
        self._money[str(unit)].pop()

    @property
    def money(self) -> Dict[str, MoneyUnit]:
        return self._money



