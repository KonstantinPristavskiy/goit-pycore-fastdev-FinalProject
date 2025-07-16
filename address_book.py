from collections import UserDict
from datetime import datetime
import re

class Field:
    """Базовий клас для всіх полів запису (ім'я, телефон, і т.д.)."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    """Клас для зберігання імені контакту."""
    pass

class Phone(Field):
    """Клас для зберігання номера телефону. Перевіряє, що номер складається з 10 цифр."""
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must have exactly 10 digits.")
        super().__init__(value) 
        
class Birthday(Field):
    """Клас для зберігання дня народження. Перевіряє формат DD.MM.YYYY."""
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Address(Field):
    """Клас для зберігання адреси."""
    def __init__(self, value):
        if not value:
            raise ValueError("Address cannot be empty")
        else:
            super().__init__(value)

class Email(Field):
    """Клас для зберігання email. Перевіряє валідність формату."""
    def __init__(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Invalid email format")
        super().__init__(value)


class Record:
    """Клас для зберігання повної інформації про контакт, включаючи ім'я, телефони та інші поля."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_phone(self, phone):
        """Додає номер телефону до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видаляє номер телефону із запису."""
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        """Редагує існуючий номер телефону."""
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        """Знаходить номер телефону в записі."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def set_birthday(self, birthday):
        """Встановлює день народження."""
        self.birthday = Birthday(birthday)

    def remove_birthday(self):
        """Видаляє день народження."""
        self.birthday = None

    def set_address(self, address):
        """Встановлює адресу."""
        self.address = Address(address)

    def remove_address(self):
        """Видаляє адресу."""
        self.address = None

    def set_email(self, email):
        """Встановлює email."""
        self.email = Email(email)

    def remove_email(self):
        """Видаляє email."""
        self.email = None

    def __str__(self):
        """Повертає рядкове представлення запису."""
        phones = '; '.join(p.value for p in self.phones)
        bday = f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else "" 
        address = f", Address: {self.address.value}" if self.address else ""
        email = f", Email: {self.email.value}" if self.email else ""
        return f"Contact name: {self.name.value}, phones: {phones}{bday}{address}{email}"
    
class AddressBook(UserDict):
    """Клас для зберігання та управління записами в адресній книзі."""
    def add_record(self, record):
        """Додає новий запис до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name):
        """Знаходить запис за іменем."""
        return self.data.get(name)

    def delete(self, name):
        """Видаляє запис за іменем."""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        """
        Повертає список контактів, у яких день народження протягом наступних days днів.
        Якщо days не вказано, за замовчуванням використовується 7 днів.
        """
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                delta = (bday - today).days
                if 0 <= delta <= days:
                    upcoming.append(f"{record.name.value} ({bday.strftime('%d.%m')})")
        return upcoming

    def search_contacts(self, query):
        """Шукає контакти за запитом у всіх полях."""
        results = set()
        query = query.lower()
        for record in self.data.values():
            if query in record.name.value.lower():
                results.add(record)
            for phone in record.phones:
                if query in phone.value:
                    results.add(record)
            if record.address and query in record.address.value.lower():
                results.add(record)
            if record.email and query in record.email.value.lower():
                results.add(record)
            if record.birthday and query in record.birthday.value.strftime('%d.%m.%Y'):
                results.add(record)
        return list(results)

        
            