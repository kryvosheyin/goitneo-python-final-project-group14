from classes.note.note_title import Title
from classes.note.note_body import NoteBody
from classes.note.note_tags import Tag


class Note:
    def __init__(self, title: Title, body: NoteBody = None):
        self.title = Title(title)
        self.body = NoteBody(body)
        self.tags = []

    def add_note(self, note_text):
        self.body = NoteBody(note_text)

    def edit_note(self, new_text):
        existing_text = str(self.body.value)
        self.body = NoteBody(str(existing_text) + "\n" + new_text)
        return self

    def add_tag(self, tag):
        if tag not in (t.value for t in self.tags):
            self.tags.append(Tag(tag))

    def get_note_tags(self):
        return ";".join(tag.value for tag in self.tags)

    def extract_tags(self):
        if self.body:
            words = str(self.body.value).split()
            for word in words:
                if word.startswith("#"):
                    self.add_tag(word[1:])

    def __str__(self) -> str:
        return f"Note title: {self.title.value}, note text: {self.body.value}"
