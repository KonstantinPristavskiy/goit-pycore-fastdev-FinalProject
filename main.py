from storage import load_book, save_book, FILENAME
from handlers import (
    add_contact, change_contact, delete_contact,
    show_phone, add_birthday, show_birthday,
    birthdays, show_all, show_help
)


def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


def main():
    book = load_book()
    print("👋 Welcome to the assistant bot!")

    while True:
        user_input = input("📝 Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_book(book)
            print(f"✅ Contacts saved to {FILENAME}")
            print("👋 Good bye!")
            break

        elif command == "hello":
            print("🤖 How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "all":
            print(show_all(book))

        elif command in ["help", "?"]:
            print(show_help())

        else:
            print("❗ Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
