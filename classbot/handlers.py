from address_book import Record, AddressBook
from decorators import input_error
from notebook import Note, NoteBook

@input_error
def contact_set(args, book: AddressBook):
    """
    Створює новий контакт або оновлює існуючий.
    contact set <name> - створює контакт
    contact set <name> <field> <value> - встановлює поле
    """
    if not args:
        return "Usage: contact set <name> [field] [value]"
    
    name = args[0]  # Ім'я завжди перший аргумент
    
    # Якщо тільки ім'я - створюємо контакт
    if len(args) == 1:
        if book.find(name):
            return f"❌ Contact '{name}' already exists"
        record = Record(name)
        book.add_record(record)
        return f"✅ Contact '{name}' created"
    
    # Якщо 3 аргументи - встановлюємо поле
    if len(args) == 3:
        field = args[1].lower()
        value = args[2]
        
        # Створюємо контакт якщо не існує
        record = book.find(name)
        if not record:
            record = Record(name)
            book.add_record(record)
        
        # Встановлюємо поле
        if field == 'phone':
            record.add_phone(value)
        elif field == 'email':
            record.set_email(value)
        elif field == 'address':
            record.set_address(value)
        elif field == 'birthday':
            record.set_birthday(value)
        else:
            return f"❌ Unknown field '{field}'. Use: phone, email, address, birthday"
        
        return f"✅ {field} set for '{name}'"
    
    return "❌ Wrong number of arguments. Use: contact set <name> OR contact set <name> <field> <value>"

@input_error
def contact_get(args, book: AddressBook):
    """
    Показує інформацію про контакти.
    contact get all - всі контакти
    contact get birthdays - дні народження (7 днів)
    contact get birthdays 10 - дні народження (10 днів)
    contact get John - знайти контакт John
    """
    if not args:
        return "Usage: contact get <all|birthdays|name>"
    
    first_arg = args[0].lower()
    
    # Показати всі контакти
    if first_arg == 'all':
        if not book.data:
            return "Address book is empty"
        return '\n'.join(str(record) for record in book.data.values())
    
    # Показати дні народження
    if first_arg == 'birthdays':
        days = 7  # за замовчуванням 7 днів
        if len(args) > 1 and args[1].isdigit():
            days = int(args[1])
        
        upcoming = book.get_upcoming_birthdays(days)
        if upcoming:
            return f"Birthdays in {days} days:\n" + "\n".join(upcoming)
        return f"No birthdays in the next {days} days"
    
    # Знайти конкретний контакт
    name = args[0]
    record = book.find(name)
    if record:
        return str(record)
    
    # Пошук по всіх полях
    results = book.search_contacts(name)
    if results:
        return "Found contacts:\n" + "\n".join(str(r) for r in results)
    
    return f"Contact '{name}' not found"

@input_error
def contact_delete(args, book: AddressBook):
    """
    Видаляє контакт або частину контакту.
    contact delete John - видаляє весь контакт
    contact delete John phone 1234567890 - видаляє телефон
    contact delete John email - видаляє email
    contact delete John address - видаляє адресу
    contact delete John birthday - видаляє день народження
    """
    if not args:
        return "Usage: contact delete <name> [field] [value]"
    
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found"
    
    # Якщо тільки ім'я - видаляємо весь контакт
    if len(args) == 1:
        book.delete(name)
        return f"Contact '{name}' deleted"
    
    # Якщо 2 аргументи - видаляємо поле (email, address, birthday)
    if len(args) == 2:
        field = args[1].lower()
        
        if field == 'email':
            if not record.email:
                return f"'{name}' has no email to delete"
            record.remove_email()
            return f"Email deleted for '{name}'"
        
        elif field == 'address':
            if not record.address:
                return f"'{name}' has no address to delete"
            record.remove_address()
            return f"Address deleted for '{name}'"
        
        elif field == 'birthday':
            if not record.birthday:
                return f"'{name}' has no birthday to delete"
            record.remove_birthday()
            return f"Birthday deleted for '{name}'"
        
        else:
            return f"❌ Unknown field '{field}'. Use: email, address, birthday, or 'phone <number>'"
    
    # Якщо 3 аргументи - видаляємо конкретний телефон
    if len(args) == 3:
        field = args[1].lower()
        value = args[2]
        
        if field == 'phone':
            if not record.find_phone(value):
                return f"Phone '{value}' not found for '{name}'"
            record.remove_phone(value)
            return f"Phone '{value}' deleted for '{name}'"
        else:
            return f"❌ For 3 arguments, only 'phone <number>' is supported"
    
    return "❌ Wrong arguments. Use: contact delete <name> [field] [value]"
@input_error
def note_set(args, notebook: NoteBook):
    """
    Створює або оновлює нотатку.
    note set "title" "content" - створює нотатку
    note set "title" tag "tag_name" - додає тег
    note set "title" content "new_content" - оновлює зміст
    """
    if len(args) < 2:
        return "Usage: note set \"title\" \"content\" OR note set \"title\" tag \"tag_name\""
    
    title = args[0]
    
    # Якщо нотатка не існує, створюємо нову
    note = notebook.find_note(title)
    if not note:
        content = args[1] if len(args) >= 2 else ""
        note = Note(title, content)
        notebook.add_note(note)
        return f"✅ Note '{title}' created"
    
    # Оновлення існуючої нотатки
    if len(args) >= 3:
        action = args[1].lower()
        value = args[2]
        
        if action == "tag":
            try:
                note.add_tag(value)
                return f"✅ Tag '#{value}' added to note '{title}'"
            except ValueError as e:
                return f"❌ {str(e)}"
        
        elif action == "content":
            note.update_content(value)
            return f"✅ Content updated for note '{title}'"
    
    return "❌ Invalid arguments"

@input_error
def note_get(args, notebook: NoteBook):
    """
    Показує нотатки.
    note get all - всі нотатки
    note get "title" - конкретна нотатка
    note get search "query" - пошук за змістом
    note get tag "tag_name" - пошук за тегом
    """
    if not args:
        return "Usage: note get <all|title|search|tag> [value]"
    
    command = args[0].lower()
    
    if command == "all":
        if not notebook.notes:
            return "No notes found"
        return '\n'.join(str(note) for note in notebook.notes.values())
    
    elif command == "search" and len(args) > 1:
        query = args[1]
        results = notebook.search_by_content(query)
        if results:
            return f"Found {len(results)} note(s):\n" + '\n'.join(str(note) for note in results)
        return f"No notes found for query '{query}'"
    
    elif command == "tag" and len(args) > 1:
        tag = args[1]
        results = notebook.search_by_tags(tag)
        if results:
            return f"Notes with tag '#{tag}':\n" + '\n'.join(str(note) for note in results)
        return f"No notes found with tag '#{tag}'"
    
    else:
        # Пошук конкретної нотатки
        title = args[0]
        note = notebook.find_note(title)
        if note:
            return str(note)
        return f"Note '{title}' not found"

@input_error
def note_delete(args, notebook: NoteBook):
    """
    Видаляє нотатку або тег.
    note delete "title" - видаляє всю нотатку
    note delete "title" tag "tag_name" - видаляє тег
    """
    if not args:
        return "Usage: note delete \"title\" [tag \"tag_name\"]"
    
    title = args[0]
    note = notebook.find_note(title)
    if not note:
        return f"Note '{title}' not found"
    
    # Видалення тегу
    if len(args) == 3 and args[1].lower() == "tag":
        tag_name = args[2]
        note.remove_tag(tag_name)
        return f"✅ Tag '#{tag_name}' removed from note '{title}'"
    
    # Видалення всієї нотатки
    elif len(args) == 1:
        notebook.delete_note(title)
        return f"✅ Note '{title}' deleted"
    
    return "❌ Invalid arguments"


def show_help():
    """Показує довідку по командам."""
    return """Available commands:
- contact set <name>                 - Create new contact
- contact set <name> <field> <value> - Set contact field
- contact get all                    - Show all contacts  
- contact get birthdays              - Show birthdays (7 days)
- contact get birthdays <days>       - Show birthdays (custom days)
- contact get <name>                 - Find contact
- contact delete <name>              - Delete entire contact
- contact delete <name> <field>      - Delete field (email, address, birthday)
- contact delete <name> phone <number> - Delete specific phone
- help                               - Show this help
- exit                               - Save and quit

Fields: phone, email, address, birthday

Examples:
  contact set John
  contact set John phone 1234567890
  contact set John email john@example.com
  contact get John
  contact get all
  contact delete John phone 1234567890
  contact delete John email
  contact delete John birthday
  contact delete John

  NOTES:
- note set "title" "content"        - Create note
- note set "title" tag "tag_name"   - Add tag to note
- note set "title" content "text"   - Update note content
- note get all                      - Show all notes
- note get "title"                  - Show specific note
- note get search "query"           - Search notes by content
- note get tag "tag_name"           - Find notes by tag
- note delete "title"               - Delete entire note
- note delete "title" tag "tag"     - Remove tag from note

Examples:
  note set "Shopping" "Buy milk and bread"
  note set "Shopping" tag "urgent"
  note get tag "work"
  note get search "milk"
  note delete "Shopping" tag "urgent"
"""