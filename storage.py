import pickle
from address_book import AddressBook

FILENAME = "address_book.pkl"

def save_book(book):
    with open(FILENAME, "wb") as f:
        pickle.dump(book, f)

def load_book():
    try:
        with open(FILENAME, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
