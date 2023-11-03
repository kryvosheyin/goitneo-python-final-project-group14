from classes.Exceptions import (
    IncorrectNameException,
    IncorrectPhoneFormatException,
    UnableToEditPhoneException,
    BirthdayFormatException,
    IndexOutOfRangeException,
    NotFoundCommand,
    IncorrectAddressFormatException
)
from classes.AddressBook import AddressBook
from classes.Name import Name
from classes.Record import Record
from classes.Email import Email
from classes.Birthday import Birthday
from classes.birthdays import get_upcoming_birthdays
from classes.address import Address
import pickle
import difflib


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
            NotFoundCommand,
            IncorrectAddressFormatException,
        ) as err:
            return str(err)

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split(" ")
    cmd = cmd.strip().lower()
    args = [arg for arg in args if arg.strip() != ""]
    return cmd, *args


def print_hello(_, __):
    return "How can I help you?"


def print_help_message(_, __):
    print(help)


@input_error
def add_contact(address_book: AddressBook, args):
    name, phone = extract_argument(
        "Please provide name and phone", args, number_values=2)
    print(f"{name} {phone}")
    contact = Record(name)
    contact.add_phone(phone)
    address_book.add_record(contact)
    return f"Contact {name} was added"


@input_error
def add_phone(address_book: AddressBook, args):
    name, phone = extract_argument(
        "Please provide name and phone", args, number_values=2)
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
def edit_phone(contact: Record, args):
    new_phone, args = extract_argument("missing new phone value", args)
    return contact.edit_phone(new_phone)


@input_error
def edit_email(contact: Record, args):
    email, args = extract_argument("missing new email value", args)
    old_email_exists = contact.email
    contact.set_email(Email(email))
    return (
        f"Email changed for {contact.name}"
        if old_email_exists
        else f"Email added to {contact.name}"
    )


@input_error
def edit_birthday(contact: Record, args):
    date_of_birth, args = extract_argument("missing new birthday value", args)
    try:
        day, month, year = date_of_birth.split(".")
    except ValueError:
        raise ValueError(
            "Please provide name and date of birth in format DD.MM.YYY")
    contact.set_birthday(int(year), int(month), int(day))
    return f"Birthday chenged to {contact.birthday} for {contact.name}"


def edit_name(address_book: AddressBook, contact: Record, args):
    name, args = extract_argument("missing new name", args)
    address_book.delete(contact.name)
    contact.name = Name(name)
    address_book.add_record(contact)
    return f"Name changed to {contact.name}"


def edit_address(contact: Record, args):
    address = extract_argument("missing new address", args, number_values=0)
    address = " ".join(address)
    old_address_exists = contact.address
    contact.set_address(Address(address))
    return (
        f"Address changed for {contact.name}"
        if old_address_exists
        else f"Address added to {contact.name}"
    )


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
def edit(address_book: AddressBook, args):
    EDIT_COMMANDS = {
        "phone": edit_phone,
        "email": edit_email,
        "birthday": edit_birthday,
        "name": edit_name,
        "address": edit_address,
    }
    name, args = extract_argument("Please provide contact name", args)
    contact = address_book.find(name)
    command, args = extract_argument(
        f"Command is missing. Please use: edit [name] [command] [args]. Available commands: {', '.join(EDIT_COMMANDS.keys())}",
        args
    )
    predicted_command = get_closest_match(command, EDIT_COMMANDS)
    if predicted_command is None:
        raise NotFoundCommand(
            f"Could not recognize the action to apply for {name}")

    if predicted_command == "name":
        status = EDIT_COMMANDS[predicted_command.lower()](
            address_book, contact, args)
    else:
        status = EDIT_COMMANDS[predicted_command.lower()](contact, args)
    print(status)


@input_error
def show_birthday(address_book: AddressBook, args):
    contact_name = extract_name(args)
    contact = address_book.find(contact_name)
    if contact.birthday is None:
        return f"{contact.name} does not have birthday saved in the Address book"
    return contact.birthday


@input_error
def add_address(address_book: AddressBook, args):
    name, *address_args = extract_argument(
        "Please provide name and address", args, number_values=2)
    address = " ".join(address_args)
    contact = address_book.find(name)
    contact.set_address(Address(address))
    return f"Address added to {contact.name}"


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


def render_contacts(records: [Record], _):
    address_book: AddressBook = AddressBook()
    for record in records:
        address_book.add_record(record)
    get_all(address_book, _)


def birthdays(address_book: AddressBook, _):
    number_of_days = int(
        input("Please enter the number of days you want to check: "))
    birthday_dict = get_upcoming_birthdays(
        address_book.data.values(), number_of_days)
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


def extract_argument(error_msg: str, args, number_values=1):
    try:
        if number_values == 0:
            if not args:
                raise ValueError
            return args
        if number_values > 1:
            (value1, value2, *args) = args
            return (value1, value2, *args)
        (value1, *args) = args
        return (value1, args)
    except ValueError as e:
        raise ValueError(error_msg)


def extract_name(args):
    return extract_argument("Please provide contact name", args)


def save_to_file(book: AddressBook, filename: str = "address_book.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)
    return f"Address book was saved to {filename}"


@input_error
def find(book: AddressBook, args):
    try:
        search_parameter = args[0]
    except IndexError:
        raise IndexError("Please provide value to search")
    records: [Record] = book.find_all(search_parameter)
    render_contacts(records, args)


def load_from_file(filename: str = "address_book.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Saved contacts not found. Creating new Address Book")
        return AddressBook()


def get_closest_match(command, COMMANDS):
    """Returns the closest matching command from COMMANDS dictionary."""

    closest_match = difflib.get_close_matches(
        command, COMMANDS.keys(), n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None


help = """
Available commands:
Exit - 'close' or 'exit'
Start work - 'hello'
Add new contact - 'add' <name without spaces> <phone>
Add new phone - 'add-phone' <name without spaces> <phone1>,<phone2>,...
Remove phone - 'remove-phone' <name without spaces> <phone>
Edit phone - 'edit' <name without spaces> phone <phone to replace> <new phone>
Edit/add email - 'edit' <name without spaces> email <new email>
Edit/add birthday - 'edit' <name without spaces> birthday <date in format DD.MM.YYYY>
Edit name - 'edit' <name without spaces> name <new name>
Edit address - 'edit' <name without spaces> address <new address>
Get all phones for contact - 'get-phone' <name without spaces>
Find contacts by value - 'find' <value containing in any field>
Remove email - 'remove-email' <name without spaces>
Get Birthday of contact - 'show-birthday' <name without spaces>
Get list of contacts to be congratulated next week - 'birthdays'
Remove contact - 'remove' <name without spaces>
Add address - 'add-address' <name without spaces> <address> 
Print all contacts - 'all'            
        """


def main():
    address_book = load_from_file()
    COMMANDS = {
        "help": print_help_message,
        "hello": print_hello,
        "add": add_contact,
        "edit": edit,
        "add-phone": add_phone,
        "remove-phone": remove_phone,
        "get-phone": get_phone,
        "remove-email": remove_email,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "remove": remove,
        "add-address": add_address,
        "all": get_all,
        "find": find,
    }

    print("Welcome to the assistant bot!")
    print(help)
    while True:
        user_input = input("\n\nEnter a command: ").strip()
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
            predicted_command = get_closest_match(command, COMMANDS)
            if predicted_command:
                print(f"Did you mean {predicted_command}? ")
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
