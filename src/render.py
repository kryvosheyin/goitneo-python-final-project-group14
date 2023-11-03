from classes.Record import Record
from rich.console import Console
from rich.table import Table, box
from classes.help_command import HelpCommand


def render_contacts(records: [Record], title="Contacts:"):
    table = Table(title=title, show_lines=True)

    table.add_column("Name", justify="center", style="magenta")
    table.add_column("Phone", justify="center")
    table.add_column("Email", justify="center")
    table.add_column("Birthday", justify="center")
    table.add_column("Address", justify="center")
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

    console = Console()
    console.print(table)
    console.print(f"Found contacts: {len(records)}")


def render_birhtdays(dictionary: dict, days: int):
    table = Table(title=f"Birthdays in next {days} days:", show_lines=True)
    table.add_column("Day", justify="center", style="magenta")
    table.add_column("Names", justify="center")

    for day, names in dictionary.items():
        table.add_row(day, names)

    console = Console()
    console.print(table)
    if len(dictionary.keys())>0:
        console.print(f"Found days: {len(dictionary.keys())}")
    else:
        console.print(f"No one should be concratulated in {days} days") 


def render_notes(notes):
    table = Table(title=f"Notes:", show_lines=True)
    table.add_column("Title", justify="center", style="magenta")
    table.add_column("Body", justify="center")
    table.add_column("Tags", justify="center")

    for note in notes:
        table.add_row(note.title, note.body, ", ".join(note.get_note_tags()))

    console = Console()
    console.print(table)
    console.print(f"Found notes: {len(notes)}")

def render_help(commands: [HelpCommand]):
    table = Table(title=f"Avaliable commands:", show_lines=True, box=box.SQUARE_DOUBLE_HEAD)
    table.add_column("Description")
    table.add_column("Command", style="magenta")

    for cmd in commands:
        table.add_row(cmd.desc, cmd.cmd)

    console = Console()
    console.print(table)


def __get_if_empty(value):
    return str(value) if value else "-"
