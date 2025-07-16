from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must have exactly 10 digits.")
        super().__init__(value) 
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Address(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Address cannot be empty")
        else:
            super().__init__(value)

class Email(Field):
    def __init__(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Invalid email format")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_birthday(self):
        self.birthday = None

    def add_address(self, address):
        self.address = Address(address)

    def remove_address(self):
        self.address = None

    def add_email(self, email):
        self.email = Email(email)

    def remove_email(self):
        self.email = None

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        bday = f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else "" 
        address = f", Address: {self.address.value}" if self.address else ""
        email = f", Email: {self.email.value}" if self.email else ""
        return f"Contact name: {self.name.value}, phones: {phones}{bday}{address}{email}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                delta = (bday - today).days
                if 0 <= delta <= 7:
                    upcoming.append(f"{record.name.value} ({bday.strftime('%d.%m')})")
        return upcoming

        
            