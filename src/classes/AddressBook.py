from collections import UserDict
from classes.Name import Name
from classes.Record import Record
from classes.Phone import Phone
from classes.Fields import Field


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    def find(self, name: Name):
        contact = self.data.get(name)
        if contact is None:
            raise KeyError(f"Contact {name} is not found")
        return contact

    def find_all(self, value: str) -> [Record]:
        search_result = []
        test_lowercase_value = self.__test_value(value.lower())
        for record in self.data.values():
            if any(filter(lambda val: test_lowercase_value(val), self.__scalar_variables_from_record(record))) or self.__test_phones(record.phones, test_lowercase_value):
                search_result.append(record)
        return search_result

    def delete(self, record_name: Name):
        try:
            del self.data[record_name.value]
        except KeyError:
            raise KeyError("Unable to find {record_name} in the address book")

    def __test_value(self, value_in_lower: str) -> bool:
        def test(record_value) -> bool:
            return record_value and str(record_value).lower().find(value_in_lower) > -1
        return test

    def __test_phones(self, phones: [Phone], test_lower_value) -> bool:
        return phones and any(filter(lambda phone: test_lower_value(phone), phones))

    # Returns the list of field values from object of Record type.
    # Function represents the part of dynamic introspection to be able to search in all available fields without any additional development efforts
    def __scalar_variables_from_record(self, record: Record) -> [Field]:
        return list(filter(lambda value: isinstance(value, Field), record.__dict__.values()))
