from collections import UserDict
from classes.record.name_field import Name
from classes.record.contact_record import Record
from classes.record.phone_field import Phone
from classes.fields import Field
from classes.note.note import Note


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    def add_note(self, note: Note):
        self.data[str(note.title)] = note

    def filter_by_class(self, class_type):
        return {
            key: value for key, value in self.items() if isinstance(value, class_type)
        }

    def find(self, name):
        all_contacts = self.filter_by_class(Record)
        contact = all_contacts.get(name)
        if contact is None:
            raise KeyError(f"Contact {name} is not found")
        return contact

    def find_note(self, title):
        all_notes = self.filter_by_class(Note)
        note = all_notes.get(str(title))
        if note is None:
            raise KeyError(f"Note title {title} does not exist")
        return note

    def search_notes_by_tag(self, search_tag: str):
        matching_notes = []
        all_notes = self.filter_by_class(Note)
        for note in all_notes:
            note = all_notes.get(note)
            # Use direct tag value comparison instead of string manipulation
            if note and any(tag.value == search_tag for tag in note.tags):
                matching_notes.append(note)
        return matching_notes

    def delete_note(self, title):
        note = self.find_note(title)
        try:
            del self.data[str(note.title)]
        except:
            raise KeyError("Title does not exist")

    def find_all(self, value: str) -> [Record]:
        search_result = []
        test_lowercase_value = self.__test_value(value.lower())
        for record in self.data.values():
            if type(record) is Record:
                if any(
                    filter(
                        lambda val: test_lowercase_value(val),
                        self.__scalar_variables_from_record(record),
                    )
                ) or self.__test_phones(record.phones, test_lowercase_value):
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
        return list(
            filter(lambda value: isinstance(value, Field), record.__dict__.values())
        )
