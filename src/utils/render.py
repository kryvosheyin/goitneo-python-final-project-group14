from classes.record.contact_record import Record
from classes.note.note import Note
from rich.console import Console
from rich.table import Table, box
from utils.help_command import HelpCommand


def render_contacts(records: [Record], title="Contacts:"):
    table = Table(title=title, show_lines=True)

    table.add_column("Name", justify="center", style="magenta")
    table.add_column("Phone", justify="center")
    table.add_column("Email", justify="center")
    table.add_column("Birthday", justify="center")
    table.add_column("Address", justify="center")
    counter = 0
    for record in records:
        if type(record) is Record:
            record: Record = record
            table.add_row(
                __get_if_empty(record.name),
                __get_if_empty(record.get_phones_list()),
                __get_if_empty(record.email),
                __get_if_empty(record.birthday),
                __get_if_empty(record.address),
            )
            counter += 1

    console = Console()
    console.print(table)
    console.print(f"Found contacts: {counter}")


def render_birhtdays(dictionary: dict, days: int):
    table = Table(title=f"Birthdays in next {days} days:", show_lines=True)
    table.add_column("Day", justify="center", style="magenta")
    table.add_column("Names", justify="center")

    for day, names in dictionary.items():
        table.add_row(day, names)

    console = Console()
    console.print(table)
    if len(dictionary.keys()) > 0:
        console.print(f"Found days: {len(dictionary.keys())}")
    else:
        console.print(f"No one should be congratulated in {days} days")


def render_notes(notes):
    table = Table(title=f"Notes:", show_lines=True)
    table.add_column("Title", justify="center", style="magenta")
    table.add_column("Body", justify="center")
    table.add_column("Tags", justify="center")
    counter = 0
    for note in notes:
        if type(note) is Note:
            table.add_row(str(note.title), str(note.body), note.get_note_tags())
            counter += 1
    console = Console()
    console.print(table)
    console.print(f"Found notes: {counter}")


def render_help(commands: [HelpCommand]):
    table = Table(
        title=f"Avaliable commands:", show_lines=True, box=box.SQUARE_DOUBLE_HEAD
    )
    table.add_column("Description")
    table.add_column("Command", style="magenta")

    for cmd in commands:
        table.add_row(cmd.desc, cmd.cmd)

    console = Console()
    console.print(table)


def __get_if_empty(value):
    return str(value) if value else "-"
