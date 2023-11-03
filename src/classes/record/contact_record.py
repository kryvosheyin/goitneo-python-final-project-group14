
from classes.record.name_field import Name
from classes.record.phone_field import Phone
from classes.record.email_field import Email
from classes.record.birthday_field import Birthday
from classes.record.address_field import Address


class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.email: Email = None
        self.birthday: Birthday = None
        self.address: Address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

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

    def set_birthday(self, year, month, day):
        self.birthday = Birthday(year, month, day)

    def set_address(self, address: Address):
        self.address = address

    def set_email(self, email: Email):
        self.email = email

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
        # Use self.address
        address_str = str(self.address) if self.address else "Not set"
        return f"Contact name: {self.name.value}, phones: {';'.join(p.value for p in self.phones)}, birthday: {birthday_str}, address: {address_str}"
