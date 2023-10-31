from classes.Name import Name
from classes.Phone import Phone
from classes.Email import Email
from classes.Birthday import Birthday


class Record:
    def __init__(self, name: Name):
        self.name: Name = name
        self.phones: list[Phone] = []
        self.email: Email = None
        self.birthday: Birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        found = list(filter(lambda p: str(p) == str(phone), self.phones))
        for i in found:
            self.phones.remove(i)

    def add_email(self, email: Email):
        self.email = email

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
