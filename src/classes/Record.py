from classes.Name import Name
from classes.Phone import Phone
from classes.Email import Email
from classes.Birthday import Birthday
from classes.Address import Address

class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.email: Email = None
        self.birthday: Birthday = None
        self.address: Address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_email(self, email: Email):
        self.email = email

    def add_birthday(self, year, month, day):
        self.birthday = Birthday(year, month, day)

    def edit_phone(self, new_phone):
        if len(self.phones) > 1:
            response = input(
                f"There is more than one phone saved for {self.name}:\n{self.get_phones()}\nPlease pick position of the number to change: "
            )
            try:
                self.phones[int(response) - 1] = Phone(new_phone)
            except IndexError:
                raise IndexError("The number provided is not valid, please try again")
        else:
            self.phones.clear()
            self.phones.append(Phone(new_phone))

    def remove_phone(self):
        self.phones.clear()
        return str(self.phones)

    def remove_email(self):
        self.email = None

    def add_address(self, address: Address):
        self.address = address

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
        address_str = str(self.address) if self.address else "Not set"
        return f"Contact name: {self.name.value}, phones: {';' .join(p.value for p in self.phones)}, birthday: {birthday_str}, address: {address_str}"
