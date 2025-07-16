from address_book import Record, AddressBook
from decorators import input_error

@input_error
def contact_set(args, book: AddressBook):
    """
    Обробляє команду 'contact set'.
    - Якщо передано тільки ім'я, створює новий контакт.
    - Якщо передано ім'я, поле та значення, додає/оновлює поле для контакту.
    """
    if not args:
        return "Usage: contact set <name> or contact set <name> <field> <value>"

    field_keywords = ['phone', 'email', 'address', 'birthday']
    field = None
    field_index = -1

    # Пошук ключового слова поля (phone, email і т.д.) в аргументах,
    # щоб відокремити ім'я від інших частин команди.
    for i, part in enumerate(args):
        if part.lower() in field_keywords:
            field = part.lower()
            field_index = i
            break
    
    # Якщо поле не знайдено, команда розглядається як 'contact set <name>'.
    if not field:
        name = " ".join(args)
        if book.find(name):
            return f"❌ Contact '{name}' already exists."
        record = Record(name)
        book.add_record(record)
        return f"✅ Contact '{name}' created."

    # Якщо поле знайдено, розбираємо ім'я та значення.
    name = " ".join(args[:field_index])
    value_parts = args[field_index + 1:]

    if not name:
        return "❌ Contact name is missing."
    if not value_parts:
        return f"❌ Value for field '{field}' is missing."

    record = book.find(name)
    created_msg = ""
    if not record:
        record = Record(name)
        book.add_record(record)
        created_msg = f"✅ Contact '{name}' created. "

    if field == 'phone':
        record.add_phone(value_parts[0])
        return created_msg + f"📞 Phone {value_parts[0]} added to '{name}'."
    elif field == 'email':
        record.set_email(value_parts[0])
        return created_msg + f"✉️ Email for '{name}' set."
    elif field == 'address':
        value = " ".join(value_parts)
        record.set_address(value)
        return created_msg + f"📍 Address for '{name}' set."
    elif field == 'birthday':
        record.set_birthday(value_parts[0])
        return created_msg + f"🎉 Birthday for '{name}' set."

@input_error
def contact_get(args, book: AddressBook):
    """
    Обробляє команду 'contact get'.
    - 'birthdays [days]': показує майбутні дні народження.
    - 'all': показує всі контакти.
    - '<query>': шукає контакти за запитом.
    """
    if not args:
        return "Usage: contact get <name|all|birthdays [days]|query>"

    # Обробка команди 'birthdays'
    if args[0].lower() == 'birthdays':
        days = 7
        if len(args) > 1:
            try:
                days = int(args[1])
                if days <= 0:
                    return "❌ Please enter a positive number of days."
            except ValueError:
                return "❌ Invalid number of days. Please provide an integer."
        
        upcoming = book.get_upcoming_birthdays(days)
        if upcoming:
            return f"🎉 Upcoming birthdays in the next {days} days:\n" + "\n".join(upcoming)
        return f"🎉 No birthdays in the next {days} days."

    # Обробка команди 'all'
    if len(args) == 1 and args[0].lower() == 'all':
        if not book.data:
            return "📭 Address book is empty."
        return '\n'.join(str(record) for record in book.data.values())

    # Пошук за іменем або іншими полями
    query = " ".join(args)
    record = book.find(query)
    if record:
        return str(record)

    results = book.search_contacts(query)
    if results:
        return "🔎 Found contacts:\n" + "\n".join(str(record) for record in results)
    
    return f"❌ No contacts found for '{query}'."

@input_error
def contact_delete(args, book: AddressBook):
    """Видаляє контакт за іменем."""
    if not args:
        return "Usage: contact delete <name>"
    name = " ".join(args)
    if book.find(name):
        book.delete(name)
        return f"🗑️ Contact '{name}' deleted."
    else:
        return f"❌ Contact '{name}' not found."

def show_help():
    """Показує довідку по командам."""
    return """📖 Available commands:
- contact set <name>                  - Create a new contact
- contact set <name> <field> <value>  - Add/Update contact field (phone, email, address, birthday)
- contact get <name|all|search_query> - Get contact info
- contact get birthdays [days]        - Show birthdays in the next 7 days (or specified days)
- contact delete <name>               - Delete a contact
- help                              - Show this help
- close / exit                      - Save and exit
"""

