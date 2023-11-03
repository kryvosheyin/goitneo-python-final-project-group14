from classes.fields import Field
from utils.custom_exceptions import IncorrectPhoneFormatException
import re


class Email(Field):
    def __init__(self, email: str):
        Email.validate(email)
        super().__init__(email)

    def validate(email: str):
        if not re.match(r"[a-z0-9._]+@[a-z]+\.[a-z]{2,3}", email):
            raise IncorrectPhoneFormatException(
                f"string '{email}' does not match. Pattern [a-z0-9]+@[a-z]+\.[a-z]"
                + "{2,3}"
            )
