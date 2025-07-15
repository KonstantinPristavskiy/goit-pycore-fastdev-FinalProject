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


    # Словник команд для яких потрібні аргументи
    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "delete": delete_contact,   
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,  
        "all": lambda args, book: show_all(book),  
    }
    


    print("👋 Welcome to the assistant bot!")




    try:
        while True:
            user_input = input("📝 Enter a command: ")
            command, args = parse_input(user_input)  

            if command in (None, ""):
                print("Enter a command.")
                continue

            elif command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "help":
                print(show_help())

            elif command == "hello":
                print("How can I help you?")

            elif command in commands:
                print(commands[command](args, book))

            else:
                print("❗ Invalid command. Type 'help' to see available commands.")
    except KeyboardInterrupt:
        # Якщо користувач натисне Ctrl+C
        print("\n⚠️ Interrupted by user.")
    finally:
        # зберігаємо стан у файл в будь якому випадку
        print(f"✅ Contacts saved to {FILENAME}")
        print("👋 Good bye!")
        save_book(book)



if __name__ == "__main__":
    main()
