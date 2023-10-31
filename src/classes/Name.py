from classes.Exceptions import IncorrectNameException
from classes.Fields import Field


class Name(Field):
    def __init__(self, name: str):
        Name.validate(name)
        super().__init__(name)

    def validate(name: str):
        if not str:
            raise IncorrectNameException("missing required name")
