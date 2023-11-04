from classes.fields import Field
from utils.custom_exceptions import IncorrectTitleException


class Title(Field):
    def __init__(self, title):
        Title.validate(title)
        super().__init__(title)

    def validate(title: str):
        if len(title) > 120:
            raise IncorrectTitleException("Title must not exceed 120 characters")
        elif title == "":
            raise IncorrectTitleException(
                "Title has to have at least one character that is not space"
            )

    def __len__(self):
        return len(self.value)
