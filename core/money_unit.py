from decimal import *
from typing import List
from core.errors import ParkomatIncorrectMoneyValueException, ParkomatNotImplementedMoneyValueException

class MoneyUnit:
    '''
    A class to represent units of money. Coins or banknotes
    '''

    _allowed = ('0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00', '10.00', '20.00', '50.00')

    def __init__(self, value: str):
        if value in MoneyUnit._allowed:
            try:
                self._value = Decimal(value)
            except ValueError:
                raise ParkomatIncorrectMoneyValueException
        else:
            raise ParkomatNotImplementedMoneyValueException

    @property
    def value(self):
        return self._value





# class Coin(MoneyUnit):

#     def __init__(self, value: str):
#         super().__init__(value, _allowed)

# class Banknote(MoneyUnit):
#     _allowed = ('10.00', '20.00', '50.00')

#     def __init__(self, value: str):
#         super().__init__(value, _allowed)