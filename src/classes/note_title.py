from classes.Fields import Field
from classes.Exceptions import IncorrectTitleException


class Title(Field):
    def __init__(self, value):
        if len(value) > 120:
            raise IncorrectTitleException("Title must not exceed 120 characters")
        elif value == "":
            raise IncorrectTitleException(
                "Title has to have at least one character that is not space"
            )
        self.value = value

    def __len__(self):
        return len(self.value)
