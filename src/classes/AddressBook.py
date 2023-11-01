from collections import UserDict, defaultdict
from datetime import date, datetime
from classes.Name import Name
from classes.Record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: Name):
        contact = self.data.get(name)
        if contact is None:
            raise KeyError(f"Contact {name} is not found")
        return contact

    def delete(self, record_name: Record):
        self.data.pop(record_name, None)
