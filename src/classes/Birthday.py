from classes.Fields import Field
from datetime import datetime


class Birthday(Field):
    def __init__(self, birthday: str):
        self.format = "%d.%m.%Y"
        self.value = datetime.strptime(birthday, self.format)

    def __str__(self):
        return self.value.strftime(self.format) if self.value else ""
