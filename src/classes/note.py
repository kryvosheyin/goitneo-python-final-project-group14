from classes.note_title import Title
from classes.note_body import NoteBody
from classes.note_tags import Tag


class Note:
    def __init__(self, title: Title, body: NoteBody = None):
        self.title = Title(title)
        self.body: NoteBody = body
        self.tags = ["one", "two"]

    def add_note(self, note_text):
        self.body = NoteBody(note_text)

    def edit_note(self, new_text):
        existing_text = self.body.value
        self.body = NoteBody(existing_text + "\n" + new_text)

    def rename_note(self, new_title: Title):
        self.title = Title(new_title)

    def add_tag(self, tag: Tag):
        self.tags.append(tag)

    def get_note_tags(self):
        return ";".join(p for p in self.tags)

    def __str__(self) -> str:
        return f"Note title: {self.title.value}, note text: {self.body.value}"
