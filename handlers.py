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
def set_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.set_birthday(birthday)
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
def set_address(args, book: AddressBook):
    if len(args) < 2:
        return "❌ Please provide both name and address."
    name = args[0]
    address = ' '.join(args[1:])
    record = book.find(name)
    if record:
        record.set_address(address)
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
def set_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record:
        record.set_email(email)
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
- edit-contact <name> <field> <new_value> Edit contact's field (phone, address, email, birthday)
- search-contacts <query>           Search contacts by name, phone, etc.
- birthdays                         Show birthdays in next 7 days
- all                               Show all contacts
- help                              Show this help
- close / exit                      Save and exit
"""
@input_error
def search_contacts(args, book: AddressBook):
    query = " ".join(args)
    if not query:
        return "Please enter a search term."
    results = book.search_contacts(query)
    if results:
        return "🔎 Found contacts:\n" + "\n".join(str(record) for record in results)
    return "❌ No contacts found for your search."


@input_error
def edit_contact(args, book: AddressBook):
    if len(args) < 3:
        return "❌ Invalid command. Use: edit-contact <name> <field> <new_value>"

    name, field, *value_parts = args
    field = field.lower()
    
    record = book.find(name)
    if not record:
        return f"❌ Contact '{name}' not found."

    if field == 'phone':
        if len(value_parts) != 2:
            return "❌ For phone, please provide old and new numbers. Usage: edit-contact <name> phone <old_phone> <new_phone>"
        old_phone, new_phone = value_parts
        
        phone_to_edit = record.find_phone(old_phone)
        if not phone_to_edit:
            return f"❌ Phone number {old_phone} not found for '{name}'."
        
        record.edit_phone(old_phone, new_phone)
        return f"📞 Phone for '{name}' updated from {old_phone} to {new_phone}."

    elif field == 'address':
        address = " ".join(value_parts)
        if not address:
             return "❌ Address cannot be empty."
        record.set_address(address)
        return f"📍 Address for '{name}' updated."
    
    elif field == 'email':
        if len(value_parts) != 1:
            return "❌ Please provide a single email address."
        email = value_parts[0]
        record.set_email(email)
        return f"✉️ Email for '{name}' updated."
        
    elif field == 'birthday':
        if len(value_parts) != 1:
            return "❌ Please provide a single birthday in DD.MM.YYYY format."
        birthday = value_parts[0]
        record.set_birthday(birthday)
        return f"🎉 Birthday for '{name}' updated."
        
    else:
        return f"❌ Invalid field '{field}'. Available fields: phone, address, email, birthday."

