class IncorrectPhoneFormatException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect phone format: {self.message}"


class BirthdayFormatException(Exception):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"Incorrect birthday format: Allowed format for '{self.value}' is DD.MM.YYYY"


class IncorrectNameException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect name: {self.message}"


class UnableToEditPhoneException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Phone does not exist: {self.message}"


class IndexOutOfRangeException(Exception):
    def __init(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class NotFoundCommand(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class IncorrectAddressFormatException(Exception):
    def __init__(self, message="Incorrect Address Format"):
        self.message = message
        super().__init__(self.message)


class IncorrectTitleException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return self.message
