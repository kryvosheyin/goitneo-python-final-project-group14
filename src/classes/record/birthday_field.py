from classes.fields import Field
from datetime import datetime
import calendar


class Birthday(Field):
    def __init__(self, year, month, day):
        self.validate(year, month, day)
        self.year = year
        self.month = month
        self.day = day
        super().__init__(datetime(year, month, day).date())

    @staticmethod
    def validate(year, month, day):
        if not (1 <= month <= 12):
            raise ValueError("Invalid month. Must be between 1 and 12 inclusive.")

        max_days_in_month = calendar.monthrange(year, month)[1]
        if not (1 <= day <= max_days_in_month):
            raise ValueError(f"Invalid day {day} for month {month} in year {year}.")

    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def as_datetime(self):
        return self.value

    def __str__(self):
        return self.value.strftime("%d %B %Y")
