from collections import UserDict, defaultdict
from datetime import date, datetime
from classes.Name import Name
from classes.Record import Record


class AddressBook(UserDict):
    def __init__(self):
        self.data = list()

    def add_record(self, record: Record):
        self.data.append(record)

    def find(self, name: Name):
        found = list(
            filter(
                lambda record: str(record.name).lower() == str(name).lower(), self.data
            )
        )
        return found[0] if found else None

    def delete(self, name: Name):
        found = self.find(name)
        if found:
            self.data.remove(found)

    def get_birthdays_per_week(self):
        week = defaultdict(list)

        today = datetime.today().date()

        for record in filter(lambda rec: rec.birthday, self.data):
            birthday = record.birthday.value.date()
            birthday_this_year: date = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)
            delta_days = (birthday_this_year - today).days
            if delta_days <= 7:
                w_day = birthday_this_year.strftime("%A")
                if w_day in ("Sunday", "Saturday"):
                    week["Monday"].append(record)
                else:
                    week[w_day].append(record)

        return week
