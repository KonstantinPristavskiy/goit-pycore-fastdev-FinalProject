from classbot.address_book import Record, AddressBook
from classbot.decorators import input_error
from classbot.notebook import Note, NoteBook
from classbot.console import console, success, info, error, Table, Columns 
import shlex

@input_error
def contact_set(args, book: AddressBook):
    """
    Створює новий контакт або оновлює існуючий.
    contact set <name> - створює контакт
    contact set <name> <field> <value> - встановлює поле
    """
    if not args:
        return error("Usage: contact set <name> [field] [value]")
    
    name = args[0]  # Ім'я завжди перший аргумент
    
    # Якщо тільки ім'я - створюємо контакт
    if len(args) == 1:
        if book.find(name):
            return error(f" Contact '{name}' already exists")
        record = Record(name)
        book.add_record(record)
        return success(f" Contact '{name}' created")
    
    # Якщо 3 або більше аргументів - встановлюємо поле
    if len(args) >= 3:
        field = args[1].lower()
        # З'єднуємо всі аргументи після field в одне значення
        value = ' '.join(args[2:])
        
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
            return error(f" Unknown field '{field}'. Use: phone, email, address, birthday")
        
        return success(f" {field} set for '{name}'")
    
    return error(" Wrong number of arguments. Use: contact set <name> OR contact set <name> <field> <value>")

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
        return error("Usage: contact get <all|birthdays|name>")
    
    first_arg = args[0].lower()
    
    # Показати всі контакти
    if first_arg == 'all':
        if not book.data:
            return info("Address book is empty")
        console.print(f"[bold green]Total contacts: {len(book.data)}[/bold green]")
        display_contacts(book)
        return ""
    
    # Показати дні народження
    if first_arg == 'birthdays':
        days = 7  # за замовчуванням 7 днів
        if len(args) > 1 and args[1].isdigit():
            days = int(args[1])
        
        upcoming = book.get_upcoming_birthdays(days)
        if upcoming:
            return success(f"Birthdays in {days} days:\n" + "\n".join(upcoming))
        return info(f"No birthdays in the next {days} days")
    
    # Знайти конкретний контакт
    name = args[0]
    record = book.find(name)
    if record:
        return str(record)
    
    # Пошук по всіх полях
    results = book.search_contacts(name)
    if results:
        return success("Found contacts:\n" + "\n".join(str(r) for r in results))
    
    return error(f"Contact '{name}' not found")

def display_contacts(book):
    """Виводить всі контакти у вигляді таблиці."""
    table = Table(title="📒 Address Book", show_lines=True)
    table.add_column("👤 Name", style="bold cyan", no_wrap=True)
    table.add_column("📱 Phone(s)", style="white")
    table.add_column("📧 Email", style="magenta")
    table.add_column("🎂 Birthday", style="yellow")
    table.add_column("🏡 Address", style="green")

    for record in sorted(book.data.values(), key=lambda r: r.name.value.lower()):
        phones = ", ".join(p.value for p in record.phones) or "-"
        email = record.email.value if record.email else "-"
        birthday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "-"
        address = record.address.value if record.address else "-"
        table.add_row(record.name.value, phones, email, birthday, address)

    console.print(table)

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
        return error("Usage: contact delete <name> [field] [value]")
    
    name = args[0]
    record = book.find(name)
    if not record:
        return error(f"Contact '{name}' not found")
    
    # Якщо тільки ім'я - видаляємо весь контакт
    if len(args) == 1:
        book.delete(name)
        return success(f"Contact '{name}' deleted")
    
    # Якщо 2 аргументи - видаляємо поле (email, address, birthday)
    if len(args) == 2:
        field = args[1].lower()
        
        if field == 'email':
            if not record.email:
                return info(f"'{name}' has no email to delete")
            record.remove_email()
            return success(f"Email deleted for '{name}'")
        
        elif field == 'address':
            if not record.address:
                return info(f"'{name}' has no address to delete")
            record.remove_address()
            return success(f"Address deleted for '{name}'")
        
        elif field == 'birthday':
            if not record.birthday:
                return info(f"'{name}' has no birthday to delete")
            record.remove_birthday()
            return success(f"Birthday deleted for '{name}'")
        
        else:
            return error(f" Unknown field '{field}'. Use: email, address, birthday, or 'phone <number>'")
    
    # Якщо 3 аргументи - видаляємо конкретний телефон
    if len(args) == 3:
        field = args[1].lower()
        value = args[2]
        
        if field == 'phone':
            if not record.find_phone(value):
                return error(f"Phone '{value}' not found for '{name}'")
            record.remove_phone(value)
            return success(f"Phone '{value}' deleted for '{name}'")
        else:
            return error(" For 3 arguments, only 'phone <number>' is supported")
    
    return error(" Wrong arguments. Use: contact delete <name> [field] [value]")

@input_error
def note_set(args, notebook: NoteBook):
    """
    Створює або оновлює нотатку.
    note set "title" "content" - створює нотатку
    note set "title" tag "tag_name" - додає тег
    note set "title" content "new_content" - оновлює зміст
    """
    if len(args) < 2:
        return error("Usage: note set \"title\" \"content\" OR note set \"title\" tag \"tag_name\"")
    
    title = args[0]  # Лапки вже видалені shlex.split()
    
    # Якщо нотатка не існує, створюємо нову
    note = notebook.find_note(title)
    if not note:
        content = ' '.join(args[1:])  # Лапки вже видалені
        note = Note(title, content)
        notebook.add_note(note)
        return success(f" Note '{title}' created")
    
    # Оновлення існуючої нотатки
    if len(args) == 2:
        # Якщо тільки 2 аргументи - оновлюємо контент
        content = args[1]
        note.update_content(content)
        return success(f" Content updated for note '{title}'")
        
    elif len(args) >= 3:
        action = args[1].lower()
        
        if action == "tag":
            value = args[2]
            try:
                note.add_tag(value)
                return success(f" Tag '#{value}' added to note '{title}'")
            except ValueError as e:
                return error(f" {str(e)}")
        
        elif action == "content":
            value = ' '.join(args[2:])
            note.update_content(value)
            return success(f" Content updated for note '{title}'")
    
    return error(" Invalid arguments")

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
        return error("Usage: note get <all|title|search|tag> [value]")

    command = args[0].lower().strip('"')

    if command == "all":
        if not notebook.notes:
            return info("No notes found")
        console.rule("[bold magenta]🗂 All Notes")
        notes = [note.__rich__() for note in notebook.notes.values()]
        console.print(Columns(notes, equal=True, expand=True))
        return ""

    elif command == "search" and len(args) > 1:
        query = args[1].strip('"')
        results = notebook.search_by_content(query)
        if results:
            console.rule(f"[bold yellow]🔍 Found {len(results)} note(s)")
            for note in results:
                console.print(note)
                console.print()
            return ""
        return info(f"No notes found for query '{query}'")

    elif command == "tag" and len(args) > 1:
        tag = args[1].strip('"')
        results = notebook.search_by_tags(tag)
        if results:
            console.rule(f"[bold green]🏷 Notes with tag #{tag}")
            for note in results:
                console.print(note)
                console.print()
            return ""
        return info(f"No notes found with tag '#{tag}'")

    else:
        title = args[0].strip('"')
        note = notebook.find_note(title)
        if note:
            console.rule(f"[bold blue]📝 Note: {title}")
            console.print(note)
            return ""
        return error(f"Note '{title}' not found")

@input_error
def note_delete(args, notebook: NoteBook):
    """
    Видаляє нотатку або тег.
    note delete "title" - видаляє всю нотатку
    note delete "title" tag "tag_name" - видаляє тег
    """
    if not args:
        return error("Usage: note delete \"title\" [tag \"tag_name\"]")
    
    title = args[0].strip('"')  # Видаляємо лапки
    note = notebook.find_note(title)
    if not note:
        return error(f"Note '{title}' not found")  # Виправлений f-string
    
    # Видалення тегу
    if len(args) == 3 and args[1].lower() == "tag":
        tag_name = args[2].strip('"')  # Видаляємо лапки
        note.remove_tag(tag_name)
        return success(f" Tag '#{tag_name}' removed from note '{title}'")
    
    # Видалення всієї нотатки
    elif len(args) == 1:
        notebook.delete_note(title)
        return success(f" Note '{title}' deleted")
    
    return error(" Invalid arguments")


def show_help():
    """Показує довідку по командам."""
    return """[bold cyan]Available commands:[/bold cyan]
[green]CONTACTS:[/green]
- contact set name                   - Create new contact
- contact set name phone value       - Set phone field
- contact set name email value       - Set email field
- contact set name address value     - Set address field
- contact set name birthday value    - Set birthday field
- contact get all                    - Show all contacts  
- contact get birthdays days        - Show birthdays (custom days)
- contact get name                   - Find contact
- contact delete name                - Delete entire contact
- contact delete name email          - Delete email field
- contact delete name address        - Delete address field
- contact delete name birthday       - Delete birthday field
- contact delete name phone number   - Delete phone field
- help                               - Show this help
- exit                               - Save and quit


[yellow]Examples:[/yellow]
  contact set John
  contact set John phone 1234567890
  contact set John email john@example.com
  contact get John
  contact get all
  contact delete John phone 1234567890
  contact delete John email
  contact delete John birthday
  contact delete John

[green]NOTES:[/green]
- note set "title" "content"        - Create note
- note set "title" tag "tag_name"   - Add tag to note
- note set "title" content "text"   - Update note content
- note get all                      - Show all notes
- note get "title"                  - Show specific note
- note get search "query"           - Search notes by content
- note get tag "tag_name"           - Find notes by tag
- note delete "title"               - Delete entire note
- note delete "title" tag "tag"     - Remove tag from note

[yellow]Examples:[/yellow]
  note set "Shopping" "Buy milk"
  note set "Shopping" tag "urgent"
  note get tag "work"
  note get search "milk"
  note delete "Shopping" tag "urgent"
"""