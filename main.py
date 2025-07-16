from storage import load_book, save_book, FILENAME
from handlers import (
    add_name, show_contact, delete_contact,
    add_phone, remove_phone, 
    add_birthday, remove_birthday, birthdays,  
    add_address, remove_address, 
    add_email, remove_email,
    show_all, show_help
)


def parse_input(user_input):
    stripped = user_input.strip()
    if not stripped:
        return "", []
    cmd, *args = stripped.split()
    return cmd.lower(), args


def main():
    book = load_book()


    # Словник команд для яких потрібні аргументи
    commands = {
        "add": add_name,
        "show": show_contact,
        "delete": delete_contact,   
        "add-phone": add_phone,
        "remove-phone": remove_phone,
        "set-birthday": add_birthday,
        "remove-birthday": remove_birthday,
        "birthdays": birthdays,  
        "set-address": add_address,
        "remove-address": remove_address,
        "set-email": add_email,
        "remove-email": remove_email,
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
