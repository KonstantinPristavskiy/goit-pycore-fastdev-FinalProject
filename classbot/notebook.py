from datetime import datetime
from .address_book import Field


class Tag(Field):
    """Клас для зберігання тегу."""
    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Tag cannot be empty")
        super().__init__(value.strip().lower())

class Note:
    """Клас для зберігання нотатки з тегами."""
    def __init__(self, title, content=""):
        self.title = title
        self.content = content
        self.tags = []
        self.created_date = datetime.now()
        self.modified_date = datetime.now()
    
    def add_tag(self, tag):
        """Додає тег до нотатки."""
        try:
            tag_obj = Tag(tag)
            if not any(t.value == tag_obj.value for t in self.tags):
                self.tags.append(tag_obj)
                self.modified_date = datetime.now()
        except ValueError as e:
            raise e
    
    def remove_tag(self, tag):
        """Видаляє тег з нотатки."""
        self.tags = [t for t in self.tags if t.value != tag.lower()]
        self.modified_date = datetime.now()
    
    def update_content(self, content):
        """Оновлює зміст нотатки."""
        self.content = content
        self.modified_date = datetime.now()
    
    def __str__(self):
        tags_str = ', '.join(f"#{tag.value}" for tag in self.tags)
        tags_part = f" | Tags: {tags_str}" if tags_str else ""
        return f"📝 {self.title}: {self.content[:50]}{'...' if len(self.content) > 50 else ''}{tags_part}"

class NoteBook:
    """Клас для управління колекцією нотаток."""
    def __init__(self):
        self.notes = {}
    
    def add_note(self, note):
        """Додає нотатку."""
        self.notes[note.title] = note
    
    def find_note(self, title):
        """Знаходить нотатку за заголовком."""
        return self.notes.get(title)
    
    def delete_note(self, title):
        """Видаляє нотатку."""
        if title in self.notes:
            del self.notes[title]
            return True
        return False
    
    def search_by_content(self, query):
        """Шукає нотатки за змістом."""
        query = query.lower()
        results = []
        for note in self.notes.values():
            if query in note.title.lower() or query in note.content.lower():
                results.append(note)
        return results
    
    def search_by_tags(self, tag):
        """Шукає нотатки за тегом."""
        tag = tag.lower()
        results = []
        for note in self.notes.values():
            if any(t.value == tag for t in note.tags):
                results.append(note)
        return results
    
    def sort_by_tags(self):
        """Сортує нотатки за тегами."""
        return sorted(self.notes.values(), key=lambda note: [tag.value for tag in note.tags])