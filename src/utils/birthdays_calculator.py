from datetime import datetime, timedelta
from collections import defaultdict
from classes.record.contact_record import Record


def get_upcoming_birthdays(users, days):
    today = datetime.now().date()
    future_date = today + timedelta(days)

    upcoming_birthdays = defaultdict(list)

    for user in users:
        if type(user) is Record:
            if user.birthday is None:
                continue
            birthday_this_year = user.birthday.as_datetime().replace(year=today.year)
            upcoming_date = (
                birthday_this_year
                if birthday_this_year >= today
                else user.birthday.as_datetime().replace(year=today.year + 1)
            )

            if today < upcoming_date <= future_date:
                upcoming_birthdays[upcoming_date].append(str(user.name))

    return upcoming_birthdays
