from classes.Fields import Field
from classes.Exceptions import IncorrectTitleException


class Title(Field):
    def __init__(self, value):
        if len(value) > 20:
            raise IncorrectTitleException("Title must not exceed 120 characters")
        self.value = value

    def __len__(self):
        return len(self.value)
