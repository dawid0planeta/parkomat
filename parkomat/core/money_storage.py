from typing import List, Set

from parkomat.core.money_unit import MoneyUnit
from parkomat.core.errors import ParkomatFullException

class MoneyStorage:
    _coins = {'0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00'}
    def __init__(self, allowed_values: Set[str], initial_units: List[MoneyUnit]):
        self._money = {key: [] for key in allowed_values}
        for unit in initial_units:
            self._money[str(unit)].append(unit)

    @property
    def money(self):
        return self._money

    def put_money(self, unit: MoneyUnit) -> None:
        str_unit = str(unit)
        if str_unit not in self._coins or len(self._money[str_unit]) < 200:
            self._money[str_unit].append(unit)
        else:
            raise ParkomatFullException

    def remove_money(self, unit: MoneyUnit) -> None:
        self._money[str(unit)].pop()



