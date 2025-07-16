import pickle
from address_book import AddressBook
from notebook import NoteBook

FILENAME = "address_book.pkl"

def save_book(book):
    """Зберігає адресну книгу у файл за допомогою pickle."""
    with open(FILENAME, "wb") as f:
        pickle.dump(book, f)

def load_book():
    """
    Завантажує адресну книгу з файлу.
    Якщо файл не знайдено, створює нову порожню адресну книгу.
    """
    try:
        with open(FILENAME, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def save_data(data):
    """Зберігає всі дані (контакти та нотатки) у файл."""
    with open(FILENAME, "wb") as f:
        pickle.dump(data, f)

def load_data():
    """Завантажує всі дані з файлу."""
    try:
        with open(FILENAME, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {'contacts': AddressBook(), 'notes': NoteBook()}