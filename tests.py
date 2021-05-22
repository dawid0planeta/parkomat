import unittest
from datetime import datetime, date, timedelta, time

from parkomat.core import MoneyUnit, Parkomat
from parkomat.core.errors import *


class TestParkomat(unittest.TestCase):
    parkomat = Parkomat()

    def test_inccorect_time_set(self):
        '''
        Test if Clock will throw an error given incorrect time
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), datetime.now().time())

        with self.assertRaises(ParkomatIncorrectTimeException):
            self.parkomat.curr_time = '34:67:94'

        self.parkomat.curr_time = '12:34:00'

    def test_single_day_leave_time_calculation(self):
        '''
        Test if leave time calculations for a single day are correct
        '''
        self.parkomat.reset()

        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(12, 34, 00))
        self.parkomat.put_money(MoneyUnit('2.00'))
        self.assertEqual(self.parkomat.leave_time, self.parkomat.curr_time + timedelta(minutes=60))

        self.parkomat.put_money(MoneyUnit('2.00'))
        self.parkomat.put_money(MoneyUnit('2.00'))
        self.assertEqual(self.parkomat.leave_time, self.parkomat.curr_time + timedelta(minutes=120))

        self.parkomat.put_money(MoneyUnit('5.00'))
        self.assertEqual(self.parkomat.leave_time, self.parkomat.curr_time + timedelta(minutes=180))

        self.parkomat.put_money(MoneyUnit('5.00'))
        self.assertEqual(self.parkomat.leave_time, self.parkomat.curr_time + timedelta(minutes=240))

    def test_overnight_leave_time_calculations(self):
        '''
        Test if leave time calculations are correct overnight
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(17, 20, 00))
        self.parkomat.put_money(MoneyUnit('2.00'))
        self.parkomat.put_money(MoneyUnit('2.00'))
        self.parkomat.put_money(MoneyUnit('2.00'))

        #check if leave time after 19
        self.assertEqual(self.parkomat.leave_time.hour, 19)

        self.parkomat.put_money(MoneyUnit('5.00'))
        self.assertEqual(self.parkomat.leave_time, datetime(2021, 5, 25, 8, 20, 00))

    def test_overweekend_leave_time_calculations(self):
        '''
        Test if leave time calculations are correct over the weekend
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(17, 20, 00))

        self.parkomat.put_money(MoneyUnit('2.00'))
        self.parkomat.put_money(MoneyUnit('2.00'))
        self.parkomat.put_money(MoneyUnit('2.00'))

        for _ in range(4):
            self.parkomat.put_money(MoneyUnit('50.00'))
            self.parkomat.put_money(MoneyUnit('10.00'))

        #check if leave time on friday
        self.assertEqual(self.parkomat.leave_time.weekday(), 4)

        self.parkomat.put_money(MoneyUnit('5.00'))
        self.assertEqual(self.parkomat.leave_time, datetime(2021, 5, 31, 8, 20, 00))

    def test_fractional_leave_time_calculations(self):
        '''
        Test if leave time calculations are correct for fractional parts of an hour
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(17, 20, 00))

        self.parkomat.put_money(MoneyUnit('1.00'))

        self.assertEqual(self.parkomat.leave_time, datetime(2021, 5, 24, 17, 50, 00))

    def test_leave_time_calculations_with_small_coins(self):
        '''
        Test if leave time calculations are correct using small value coins
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(17, 20, 00))

        for _ in range(200):
            self.parkomat.put_money(MoneyUnit('0.01'))

        self.assertEqual(self.parkomat.leave_time, datetime(2021, 5, 24, 18, 20, 00))

    def test_money_storage_full_error(self):
        '''
        Test if giving over 200 same coins to MoneyStorage will trigger an error
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(17, 20, 00))

        with self.assertRaises(ParkomatFullException):
            for _ in range(201):
                self.parkomat.put_money(MoneyUnit('0.01'))


    def test_no_coins_given_error(self):
        '''
        Test if trying to buy ticket without giving any coins will trigger an error
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(17, 20, 00))
        self.parkomat.registration_number = "KBR1234"

        self.assertRaises(ParkomatNoMoneyInsertedException, self.parkomat.buy)

    def test_incorrect_registration_number_error(self):
        '''
        Test if trying to buy ticket without giving a proper registration number will trigger an error
        '''
        self.parkomat.reset()
        self.parkomat._clock._curr_time = datetime.combine(date(2021, 5, 24), time(17, 20, 00))
        self.parkomat.put_money(MoneyUnit('2.00'))

        self.parkomat.registration_number = ""
        self.assertRaises(ParkomatEmptyRegistrationNumberException, self.parkomat.buy)

        self.parkomat.registration_number = "dss&&"
        self.assertRaises(ParkomatIncorrectRegistrationNumberException, self.parkomat.buy)


if __name__ == '__main__':
    unittest.main(verbosity=2)