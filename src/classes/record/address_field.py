from classes.fields import Field
from utils.custom_exceptions import IncorrectAddressFormatException


class Address(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value:
            raise IncorrectAddressFormatException("Address cannot be empty")

    def __str__(self):
        return self.value
