from classes.fields import Field
from utils.custom_exceptions import IncorrectPhoneFormatException
import re


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise IncorrectPhoneFormatException("Phone number must be 10 digits")
