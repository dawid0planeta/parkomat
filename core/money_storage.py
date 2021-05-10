from typing import List
from core.money_unit import MoneyUnit

class MoneyStorage:
    def __init__(self, allowed_values: List[str], initial_units: List[MoneyUnit]):
        self._money = {key: [] for key in allowed_values}
        for unit in initial_units:
            self._money[str(unit.value)].append(unit)

    @property
    def money(self):
        return self._money
