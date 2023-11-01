from collections import UserDict, defaultdict
from datetime import date, datetime
from classes.Name import Name
from classes.Record import Record
from classes.Note import Note
import pickle
# ОЛЯ.Збереження notes на жорсткий диск 
import os
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_directory)

sys.path.insert(0, project_root)

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: Name):
        contact = self.data.get(name)
        if contact is None:
            raise KeyError(f"Contact {name} is not found")
        return contact

    def delete(self, record_name: Name):
        try:
            del self.data[record_name.value]
        except KeyError:
            raise KeyError("Unable to find {record_name} in the address book")
        
    # ОЛЯ. Методи для роботи з нотатками:
    def add_note(self, note):
        self.notes[note.title] = note
        self.save_notes(os.path.join(project_root, 'data', 'notes.data.txt')) #ЯКИЙ ЗРОБИМО ШЛЯХ ЗБЕРІГАННЯ НОТАТКІВ

    def find_notes(self, query):
        found_notes = []
        for title, note in self.notes.items():
            if query in title or query in note.text or any(tag for tag in note.tags if query in tag):
                found_notes.append(note)
        return found_notes if found_notes else "nothing found"

    def remove_note(self, title):
        if title in self.notes:
            del self.notes[title]

    def edit_note(self, title, new_text):
        note = self.find_note(title)
        if note:
            note.text = new_text
    # АБО ТАК? def edit_note(self, title, new_text):
    #note = self.find_note(title)
    #if note:
        #note.text = new_text
        #return True
    #return False

    def find_note(self, title):
        return self.notes.get(title, None)
    
    def save_notes(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.notes, file)

    def load_notes(self, filename):
        with open(filename, 'rb') as file:
            self.notes = pickle.load(file)
