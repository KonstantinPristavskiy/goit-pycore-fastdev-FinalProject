from address_book import Record, AddressBook
from decorators import input_error

@input_error
def contact_set(args, book: AddressBook):
    """
    Створює новий контакт або оновлює існуючий.
    contact set <name> - створює контакт
    contact set <name> <field> <value> - встановлює поле
    contact set <name> phone <old_phone> <new_phone> - редагує телефон
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
    
    # Якщо 4 аргументи - редагуємо телефон
    if len(args) == 4:
        field = args[1].lower()
        old_phone = args[2]
        new_phone = args[3]
        
        if field != 'phone':
            return f"❌ Edit only works for phone. Use: contact set {name} phone <old> <new>"
        
        record = book.find(name)
        if not record:
            return f"❌ Contact '{name}' not found"
        
        # Перевіряємо чи є старий номер
        if not record.find_phone(old_phone):
            return f"❌ Phone '{old_phone}' not found for '{name}'"
        
        # Редагуємо телефон
        record.edit_phone(old_phone, new_phone)
        return f"✅ Phone changed from '{old_phone}' to '{new_phone}' for '{name}'"
    
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
    Видаляє контакт.
    contact delete John
    """
    if not args:
        return "Usage: contact delete <name>"
    
    name = args[0]
    if book.find(name):
        book.delete(name)
        return f"Contact '{name}' deleted"
    
    return f"Contact '{name}' not found"

def show_help():
    """Показує довідку по командам."""
    return """Available commands:
- contact set <name>                 - Create new contact
- contact set <name> <field> <value> - Set contact field
- contact set <name> phone <old> <new> - Edit phone number
- contact get all                    - Show all contacts  
- contact get birthdays              - Show birthdays (7 days)
- contact get birthdays <days>       - Show birthdays (custom days)
- contact get <name>                 - Find contact
- contact delete <name>              - Delete contact
- help                               - Show this help
- exit                               - Save and quit

Fields: phone, email, address, birthday

Examples:
  contact set John
  contact set John phone 1234567890
  contact set John email john@example.com
  contact set John phone 1234567890 0987654321
  contact get John
  contact get all
  contact delete John
"""