from classes.Fields import Field
from classes.Exceptions import IncorrectTitleException


class Title(Field):
    def __init__(self, value):
        if len(self.value) > 120 or type(self.value) is not str:
            raise IncorrectTitleException("Title must not exceed 120 characters")
        self.value = value
