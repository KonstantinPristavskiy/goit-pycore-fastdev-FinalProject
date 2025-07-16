from address_book import Record, AddressBook
from decorators import input_error


@input_error
def add_name(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return f"🔁 Contact '{name}' already exists."
    else:
        record = Record(name)
        book.add_record(record)
        return f"✅ Contact '{name}' added."


@input_error
def show_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return str(record)
    return f"❌ Contact '{name}' not found."



@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    if book.find(name):
        book.delete(name)
        return f"🗑️ Contact '{name}' deleted."
    else:
        return f"❌ Contact '{name}' not found."





@input_error
def add_phone(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
        return f"🔁 Phone number {phone} added to '{name}'."
    else:
        return f"❌ Contact '{name}' not found."



@input_error
def remove_phone(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if record:
        phone_obj = record.find_phone(phone)
        if phone_obj:
            record.remove_phone(phone)
            return f"🔁 Phone number {phone} removed from '{name}'."
        else:
            return f"❌ Phone number {phone} not found for '{name}'."
    else:  
        return f"❌ Contact '{name}' not found."



@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"🎉 Birthday added for '{name}'."
    return f"❌ Contact '{name}' not found."


@input_error
def remove_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        record.remove_birthday()
        return f"🎉 Birthday removed for '{name}'."
    return f"❌ Contact '{name}' not found."



@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if upcoming:
        return "🎉 Upcoming birthdays:\n" + "\n".join(upcoming)
    return "🎉 No birthdays in the next week."


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "📭 Address book is empty."

    return '\n'.join(str(record) for record in book.data.values())


@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        return "❌ Please provide both name and address."
    name = args[0]
    address = ' '.join(args[1:])
    record = book.find(name)
    if record:
        record.add_address(address)
        return f"📍 Address added for '{name}'."
    return f"❌ Contact '{name}' not found."



@input_error
def remove_address(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        record.remove_address()
        return f"📍 Address removed for '{name}'."
    return f"❌ Contact '{name}' not found."


@input_error
def add_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return f"✉️ Email added for '{name}'."
    return f"❌ Contact '{name}' not found."


@input_error
def remove_email(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        record.remove_email()
        return f"✉️ Email removed for '{name}'."
    return f"❌ Contact '{name}' not found."





def show_help():
    return """📖 Available commands:
- add <name>                        Add new contact
- show <name>                       Show contact
- delete <name>                     Delete contact
- add-phone <name> <phone>          Add phone to contact
- remove-phone <name> <phone>       Remove phone from contact
- set-address <name> <address>      Set address for contact
- remove-address <name>             Remove address from contact
- set-email <name> <email>          Set email for contact
- remove-email <name>               Remove email from contact
- set-birthday <name> <DD.MM.YYYY>  Set birthday for contact (DD.MM.YYYY)
- remove-birthday <name>            Remove birthday from contact
- birthdays                         Show birthdays in next 7 days
- all                               Show all contacts
- help                              Show this help
- close / exit                      Save and exit
"""
