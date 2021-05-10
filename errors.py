class ParkomatException(Exception):
    '''
    General class for all exceptions in Parkomat program
    '''

class ParkomatIncorrectMoneyValueException(ParkomatException):
    '''
    Exception raised if value given to MoneyUnit cannot be expressed in Decimal
    '''

class ParkomatNotImplementedMoneyValueException(ParkomatException):
    '''
    Exception raised if value given to MoneyUnit is not allowed by this Parkomat
    '''