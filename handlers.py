from address_book import Record, AddressBook
from decorators import input_error


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "🔁 Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "✅ Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"🔁 Phone number updated for '{name}'."
    else:
        return f"❌ Contact '{name}' not found."


@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    book.delete(name)
    return f"🗑️ Contact '{name}' deleted."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return f"📞 {name}'s phone(s): {phones}"
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
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"🎂 {name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}."
    elif record:
        return f"⚠️ {name} does not have a birthday set."
    else:
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

    return '\n'.join(str(record) for record in book.data.values()) if book.data else "📭 Address book is empty."


def show_help():
    return """📖 Available commands:
- add <name> <phone>            Add new contact or phone to existing
- change <name> <old> <new>     Change phone number
- delete <name>                 Delete contact
- phone <name>                  Show phones for contact
- add-birthday <name> <DD.MM.YYYY> Add birthday
- show-birthday <name>          Show birthday
- birthdays                     Show birthdays in next 7 days
- all                           Show all contacts
- help                          Show this help
- close / exit                  Save and exit
"""
