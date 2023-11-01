

class Note:
    def __init__(self, title, text, tags=None):
        self.title = title
        self.text = text
        self.tags = tags if tags else []

    def __init__(self):
        self.notes = {}
        # І якщо треба буде завантажити нотатки:
        # self.load_notes('../data/notes.data.txt')