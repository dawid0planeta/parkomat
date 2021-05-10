from decimal import Decimal

from core import MoneyUnit, MoneyStorage

allowed = ('0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00', '10.00', '20.00', '50.00')

def test_money_unit():
    for each in allowed:
        assert MoneyUnit(each).value == Decimal(each)


def test_money_storage():
    test_money_str = ['0.01', '0.01', '0.50', '0.20', '0.20', '0.50', '1.00', '1.00', '5.00', '10.00', '20.00', '50.00']
    test_money_objects = [MoneyUnit(unit) for unit in test_money_str]
    storage = MoneyStorage(allowed, test_money_objects)
    expected = {
        '0.01': [test_money_objects[0], test_money_objects[1]],
        '0.02': [],
        '0.05': [],
        '0.10': [],
        '0.20': [test_money_objects[3], test_money_objects[4]],
        '0.50': [test_money_objects[2], test_money_objects[5]],
        '1.00': [test_money_objects[6], test_money_objects[7]],
        '2.00': [],
        '5.00': [test_money_objects[8]],
        '10.00': [test_money_objects[9]],
        '20.00': [test_money_objects[10]],
        '50.00': [test_money_objects[11]],
    }

    assert storage.money == expected

test_money_unit()
test_money_storage()