from classes.Fields import Field
from classes.Exceptions import IncorrectPhoneFormatException
import re


class Phone(Field):
    def __init__(self, phone: str):
        Phone.validate(phone)
        super().__init__(phone)

    def update_value(self, new_value: str):
        Phone.validate(new_value)
        self.value = new_value

    def validate(phone: str):
        if not re.match(r"\d{10}", phone):
            raise IncorrectPhoneFormatException(
                f"string '{phone}' does not match. Allowed digits only, lenght 10 digits"
            )
