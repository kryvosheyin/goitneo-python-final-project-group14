from classes.Name import Name
from classes.Phone import Phone
from classes.Email import Email
from classes.Birthday import Birthday

class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.email: Email = None
        self.birthday: Birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, year, month, day):
        self.birthday = Birthday(year, month, day)

    def edit_phone(self, new_phone):
        if len(self.phones) > 1:
            response = input(
                f"There is more than one phone saved for {self.name}:\n{self.get_phones()}\nPlease pick position of the number to change: "
            )
            try:
                old_phone = self.phones[int(response) - 1]
                self.phones[int(response) - 1] = Phone(new_phone)
                return f"Phone from {old_phone} changed to {new_phone} for {self.name}"
            except IndexError:
                raise IndexError("The number provided is not valid, please try again")
        elif len(self.phones) == 1:
            old_phone = self.phones[0]
            self.phones[0] = Phone(new_phone)
            return f"Phone from {old_phone} changed to {new_phone} for {self.name}"
        else:
            self.phones.append(Phone(new_phone))
            return f"Phone {new_phone} added for {self.name}"

    def remove_phone(self):
        self.phones.clear()
        return str(self.phones)

    def remove_email(self):
        self.email = None

    def get_phones_list(self):
        return ";".join(p.value for p in self.phones)

    def get_phones(self):
        if len(self.phones) == 0:
            return f"There are no phones saved for {self.name}"
        return "\n".join(
            f"{index+1}. {phone.value}" for index, phone in enumerate(self.phones)
        )

    def __str__(self):
        birthday_str = str(self.birthday) if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {';' .join(p.value for p in self.phones)}, birthday: {birthday_str}"
