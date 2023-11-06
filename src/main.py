from utils.custom_exceptions import (
    IncorrectNameException,
    IncorrectPhoneFormatException,
    UnableToEditPhoneException,
    BirthdayFormatException,
    IndexOutOfRangeException,
    NotFoundCommand,
    IncorrectAddressFormatException,
    IncorrectTitleException,
)
from classes.address_book import AddressBook
from classes.record.name_field import Name
from classes.record.contact_record import Record
from classes.record.email_field import Email
from utils.birthdays_calculator import get_upcoming_birthdays
from classes.record.address_field import Address
from utils.help_command import HelpCommand
from classes.note.note import Note
from classes.note.note_body import NoteBody
from classes.note.note_title import Title
import pickle
import difflib
import utils.render as render
from rich.console import Console


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
            IncorrectTitleException,
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


def print_help_message(_, args):
    search_arg = " ".join(args).lower()
    print(search_arg)
    result = []
    for i in help:
        if i.desc.lower().find(search_arg) > -1 or i.cmd.lower().find(search_arg) > -1:
            result.append(i)
    render.render_help(result)


@input_error
def add_contact(address_book: AddressBook, args):
    name, phone, *args = extract_argument(
        "Please provide name and phone", args, number_values=2
    )
    contact = Record(name)
    contact.add_phone(phone)
    address_book.add_record(contact)
    return f"Contact {name} was added"


@input_error
def add_phone(address_book: AddressBook, args):
    name, phone, *args = extract_argument(
        "Please provide name and phone", args, number_values=2
    )
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
        raise ValueError("Please provide name and date of birth in format DD.MM.YYY")
    contact.set_birthday(int(year), int(month), int(day))
    return f"Birthday changed to {contact.birthday} for {contact.name}"


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
        args,
    )
    predicted_command = get_closest_match(command, EDIT_COMMANDS)
    if predicted_command is None:
        raise NotFoundCommand(f"Could not recognize the action to apply for {name}")

    if predicted_command == "name":
        status = EDIT_COMMANDS[predicted_command.lower()](address_book, contact, args)
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
        "Please provide name and address", args, number_values=2
    )
    address = " ".join(address_args)
    contact = address_book.find(name)
    contact.set_address(Address(address))
    return f"Address added to {contact.name}"


def get_all(address_book: AddressBook, _):
    render.render_contacts(address_book.data.values())


def render_contacts(records: [Record], _):
    render.render_contacts(records, title="Found contacts:")


def birthdays(address_book: AddressBook, _):
    number_of_days = int(input("Please enter the number of days you want to check: "))

    birthday_dict = get_upcoming_birthdays(address_book.data.values(), number_of_days)
    result = {}
    if birthday_dict:
        sorted_days = sorted(birthday_dict)
        for day in sorted_days:
            if day in birthday_dict:
                result[day.strftime("%d %B")] = ", ".join(birthday_dict[day])
    render.render_birhtdays(result, number_of_days)


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
    return extract_argument("Please provide contact name", args)[0]


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


@input_error
def add_note(address_book: AddressBook, args):
    title_args = " ".join(args).strip()
    title = Title(title_args.strip())
    body_input = multi_line_input("Please enter the note text:")
    body = NoteBody(body_input)
    note = Note(title, body)
    note.extract_tags()
    address_book.add_note(note)
    return "Your note is successfully saved"


def multi_line_input(prompt="Enter text (press Enter twice to finish): "):
    print(prompt)
    input_lines = []

    while True:
        line = input().strip()
        if line == "":
            if input_lines and input_lines[-1] == "":
                input_lines.pop()  # Remove the last empty line
                break
            elif not input_lines:
                break  # Stop if the first input is a double enter
        input_lines.append(line)

    text = "\n".join(input_lines)
    return text


def print_notes(address_book: AddressBook, _):
    render.render_notes(address_book.data.values())


@input_error
def find_note_by_tag(address_book: AddressBook, search_tag):
    tag = extract_name(search_tag)
    render.render_notes(address_book.search_notes_by_tag(tag))


@input_error
def delete_note(address_book: AddressBook, args):
    title_args = " ".join(args).strip()
    address_book.delete_note(title_args)
    return "Note was deleted"


@input_error
def find_note(address_book: AddressBook, args):
    title_args = " ".join(args).strip()
    notes_list = list()
    notes_list.append(address_book.find_note(title_args))
    render.render_notes(notes_list)


@input_error
def edit_note(address_book: AddressBook, args):
    title_args = " ".join(args).strip()
    note = address_book.find_note(title_args)
    note.edit_note(multi_line_input())


def load_from_file(filename: str = "address_book.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("Saved contacts not found. Creating new Address Book")
        return AddressBook()


def get_closest_match(command, COMMANDS):
    """Returns the closest matching command from COMMANDS dictionary."""

    closest_match = difflib.get_close_matches(command, COMMANDS.keys(), n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None


help = [
    HelpCommand("Exit", "'close' or 'exit'"),
    HelpCommand("Start work", "'hello'"),
    HelpCommand("Get help. List of available commands", "'help'"),
    HelpCommand("Get help. Search commands by text", "'help' {value to search}"),
    HelpCommand("Add new contact", "'add' {contact's name without spaces} {phone}"),
    HelpCommand("Remove existing contact", "'remove {contact's name without spaces}"),
    HelpCommand("Find contacts by value", "'find' {value containing in any field}"),
    HelpCommand(
        "Add new phone to existing contact",
        "'add-phone' {contact's name without spaces} {phone}",
    ),
    HelpCommand(
        "Remove all phones from existing contact",
        "'remove-phone' {contact's name without spaces}",
    ),
    HelpCommand(
        "Edit phone of existing contact",
        "'edit' {contact's name without spaces} phone {new phone}",
    ),
    HelpCommand(
        "Add/edit email of existing contact",
        "'edit' {contact's name without spaces} email {new email}",
    ),
    HelpCommand(
        "Get phones of existing contact",
        "'get-phone' {contact's name without spaces}",
    ),
        HelpCommand(
        "Remove email of existing contact",
        "'remove-email' {contact's name without spaces}",
    ),
    HelpCommand(
        "Add/edit birthday of existing contact",
        "'edit' {contact's name without spaces} birthday {date in format DD.MM.YYYY}",
    ),
    HelpCommand(
        "Get birthday of existing contact",
        "'show-birthday' {contact's name without spaces}",
    ),
    HelpCommand(
        "Edit name of existing contact",
        "'edit' {contact's name without spaces} name {new name}",
    ),
    HelpCommand(
        "Add address to existing contact",
        "'add-address' {contact's name without spaces} {new address}",
    ),
    HelpCommand(
        "Edit address of existing contact",
        "'edit' {contact's name without spaces} address {new address}",
    ),
    HelpCommand("Get list of contacts to be congratulated", "'birthdays'"),
    HelpCommand("Remove existing contact", "'remove' {contact's name without spaces}"),
    HelpCommand("Print all contacts", "'all'"),
    HelpCommand(
        "Add new note", "'add-note' {note title} {note text with multiple lines}"
    ),
    HelpCommand("Print all saved notes", "'all-notes'"),
    HelpCommand("Find note by title", "'find-note' {note title}"),
    HelpCommand("Delete note by title", "'delete-note' {note title}"),
    HelpCommand("Edit note text (add to existing)", "'edit-note' {note title}"),
    HelpCommand("Search notes by tags", "'find-tag' {tag word}"),
]


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
        "add-note": add_note,
        "all-notes": print_notes,
        "find-note": find_note,
        "delete-note": delete_note,
        "edit-note": edit_note,
        "find-tag": find_note_by_tag,
    }
    console = Console()

    print("Welcome to the assistant bot!")
    render.render_help(help)
    while True:
        print(3 * "\n")
        user_input = console.input("[bold blue]Enter a command:[/] ").strip()
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Saving contacts..")
            save_to_file(address_book)
            print("Good bye!")
            break
        elif command in COMMANDS:
            result = COMMANDS[command](address_book, args)
            if result:
                console.print(f"\n[green]{result.upper() if isinstance(result, str) else result}[/]")

        else:
            predicted_command = get_closest_match(command, COMMANDS)
            if predicted_command:
                print(f"Did you mean {predicted_command}? ")
            else:
                console.print("\n[bold red]INVALID COMMAND[/]")


if __name__ == "__main__":
    main()
