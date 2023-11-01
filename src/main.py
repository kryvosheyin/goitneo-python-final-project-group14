from classes.Exceptions import (
    IncorrectNameException,
    IncorrectPhoneFormatException,
    UnableToEditPhoneException,
    BirthdayFormatException,
    IndexOutOfRangeException,
)
from classes.AddressBook import AddressBook
from classes.Name import Name
from classes.Phone import Phone
from classes.Record import Record
from classes.Email import Email
from classes.Birthday import Birthday
from classes.birthdays import get_upcoming_birthdays
import pickle


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            ValueError,
            KeyError,
            IndexError,
            IncorrectPhoneFormatException,
            IncorrectNameException,
            UnableToEditPhoneException,
            BirthdayFormatException,
            IndexOutOfRangeException,
        ) as err:
            return str(err)

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split(" ")
    cmd = cmd.strip().lower()
    return cmd, *args


def print_hello(_, __):
    return "How can I help you?"


def print_help_message(_, __):
    print(help)


@input_error
def add_contact(address_book: AddressBook, args):
    name, phone = extract_args(args)
    contact = Record(name)
    contact.add_phone(phone)
    address_book.add_record(contact)
    return f"Contact {name} was added"


@input_error
def add_phone(address_book: AddressBook, args):
    name, phone = extract_args(args)
    contact = address_book.find(name)
    contact.add_phone(phone)
    return f"Phone {phone} added to contact {contact.name}"


@input_error
def remove_phone(address_book: AddressBook, args):
    contact_name = extract_name(args)
    contact = address_book.find(contact_name)
    contact.remove_phone()
    return f"All phone numbers for {contact.name} were removed"


@input_error
def get_phone(address_book: AddressBook, args):
    contact_name = extract_name(args)
    contact = address_book.find(contact_name)
    return contact.get_phones()


@input_error
def edit_phone(address_book: AddressBook, args):
    name, phone = extract_args(args)
    contact = address_book.find(name)
    contact.edit_phone(phone)
    return f"Contact {contact.name} was updated with {phone}"


@input_error
def add_email(address_book: AddressBook, args):
    name, email = extract_args(args)
    contact = address_book.find(name)
    contact.email = Email(email)
    return f"Email added to {contact.name}"


@input_error
def change_email(address_book: AddressBook, args):
    name, email = extract_args(args)
    contact = address_book.find(name)
    contact.email = Email(email)
    return "Email changed"


@input_error
def remove_email(address_book: AddressBook, args):
    contact_name = extract_name(args)
    contact = address_book.find(contact_name)
    contact.remove_email()
    return "Email removed"


@input_error
def remove(address_book: AddressBook, args):
    contact_name = extract_name(args)
    contact = address_book.find(contact_name)
    address_book.delete(contact.name)
    return "Removed."


@input_error
def add_birthday(address_book: AddressBook, args):
    try:
        contact_name, date_of_birth = args
        day, month, year = date_of_birth.split(".")
    except ValueError:
        raise ValueError("Please provide name and date of birth in format DD.MM.YYY")
    contact = address_book.find(contact_name)
    contact.add_birthday(int(year), int(month), int(day))
    return f"{contact.name}'s birthday was added to the Address book"


@input_error
def show_birthday(address_book: AddressBook, args):
    contact_name = extract_name(args)
    contact = address_book.find(contact_name)
    if contact.birthday is None:
        return f"{contact.name} does not have birthday saved in the Address book"
    return contact.birthday


def get_all(address_book: AddressBook, _):
    print(f"{'_'*135}")
    print(f"|{'Name:':^40}|{'Phone:':^30}|{'Email:':^30}|{'Birthday:':^30}|")
    print(f"|{'_'*40}|{'_'*30}|{'_'*30}|{'_'*30}|")
    if len(address_book.data) > 0:
        for contact, contact_info in address_book.data.items():
            print(
                f"|{str(contact_info.name):^40}|{(str(contact_info.get_phones_list())):^30}|{str(contact_info.email):^30}|{str(contact_info.birthday):^30}|"
            )
            print(f"|{'_'*40}|{'_'*30}|{'_'*30}|{'_'*30}|")
    else:
        print(f"|{' '*133}|")
        print(f"|{'No records found. Add at first':^133}|")
        print(f"|{'_'*133}|")


def birthdays(address_book: AddressBook, _):
    number_of_days = int(input("Please enter the number of days you want to check: "))
    birthday_dict = get_upcoming_birthdays(address_book.data.values(), number_of_days)
    print(f"{'_'*73}")
    print(f"|{'Day:':^30}|{'Name:':^40}|")
    print(f"|{'_'*30}|{'_'*40}|")
    if birthday_dict:
        sorted_days = sorted(birthday_dict)
        for day in sorted_days:
            if day in birthday_dict:
                print(
                    f"|{day.strftime('%d %B'):30}|{', '.join(birthday_dict[day]):^40}|"
                )
                print(f"|{'_'*30}|{'_'*40}|")
    else:
        print(f"|{' '*71}|")
        print(f"|{'No matches found.':^71}|")
        print(f"|{'_'*71}|")


def extract_name(args: list):
    try:
        return args[0]
    except IndexError:
        raise IndexError("Please provide contact name")


def extract_args(args: list):
    try:
        name, phone = args
    except ValueError:
        raise ValueError("Please provide name and phone")
    return name, phone


def save_to_file(book: AddressBook, filename: str = "address_book.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)
    return f"Address book was saved to {filename}"


def load_from_file(filename: str = "address_book.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Saved contacts not found. Creating new Address Book")
        return AddressBook()


help = """
Available commands:
Exit - 'close' or 'exit'
Start work - 'hello'
Add new contact - 'add' <name without spaces> <phone>
Add new phone - 'add-phone' <name without spaces> <phone1>,<phone2>,...
Remove phone - 'remove-phone' <name without spaces> <phone>
Edit phone - 'edit-phone' <name without spaces> <phone-to-change> <phone-new>
Get all phones for contact - 'get-phone' <name without spaces>
Add email - 'add-email' <name without spaces> <email>
Change email - 'change-email' <name without spaces> <email>
Remove email - 'remove-email' <name without spaces>
Add/change Birthday - 'add-birthday' <name without spaces> <date in format DD.MM.YYYY>
Get Birthday of contact - 'show-birthday' <name without spaces>
Get list of contacts to be congratulated next week - 'birthdays'
Remove contact - 'remove' <name without spaces> 
Print all contacts - 'all'            
        """


def main():
    address_book = load_from_file()
    COMMANDS = {
        "help": print_help_message,
        "hello": print_hello,
        "add": add_contact,
        "add-phone": add_phone,
        "remove-phone": remove_phone,
        "edit-phone": edit_phone,
        "get-phone": get_phone,
        "add-email": add_email,
        "change-email": change_email,
        "remove-email": remove_email,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "remove": remove,
        "all": get_all,
    }

    print("Welcome to the assistant bot!")
    print(help)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Saving contacts..")
            save_to_file(address_book)
            print("Good bye!")
            break
        elif command in COMMANDS:
            result = COMMANDS[command](address_book, args)
            if result:
                print(result)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
