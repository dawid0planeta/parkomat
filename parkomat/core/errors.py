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

class ParkomatIncorrectTimeException(ParkomatException):
    '''
    Exception raised if value given to Clock is incorrect
    '''

class ParkomatFullException(ParkomatException):
    '''
    Exception raised if coin given to MoneyStorage won't fit
    '''

class ParkomatIncorrectRegistrationNumber(ParkomatException):
    '''
    Exception raised if registration number given to Parkomat is in inccorect format
    '''
