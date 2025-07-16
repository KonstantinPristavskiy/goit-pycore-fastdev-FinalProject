from storage import load_book, save_book, FILENAME
from handlers import (
    contact_set, contact_get, contact_delete, show_help
)
from guesser import guess_command

def parse_input(user_input):
    """
    Розбирає введений рядок на основну команду, підкоманду та аргументи.
    Приклад: "contact set John phone 123" -> ('contact', 'set', ['John', 'phone', '123'])
    """
    stripped = user_input.strip()
    if not stripped:
        return None, None, []
    
    parts = stripped.split()
    command = parts[0].lower()
    
    # Якщо команда не 'contact', то підкоманди немає.
    if command != 'contact':
        return command, None, parts[1:]

    # Якщо команда 'contact', але немає підкоманди.
    if len(parts) < 2:
        return command, None, []

    sub_command = parts[1].lower()
    args = parts[2:]
    return command, sub_command, args

def main():
    book = load_book()

    # Словник для команд, що стосуються контактів
    contact_commands = {
        "set": contact_set,
        "get": contact_get,
        "delete": contact_delete,
    }

    # тут потрібно створити словники для команд note

    
    print("👋 Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("📝 Enter a command: ")
            command, sub_command, args = parse_input(user_input)

            if not command:
                continue

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "help":
                print(show_help())
            
            # Виклик обробників для команди 'contact'
            elif command == 'contact':
                if sub_command in contact_commands:
                    print(contact_commands[sub_command](args, book))
                else:
                    suggestion = guess_command(command, sub_command)
                    if suggestion:
                        print(f"❓ Unknown contact command '{sub_command}'. Maybe you meant: '{suggestion}'?")
                    else:
                        print("Invalid contact command. Use: set, get, delete, or help.")

            
            else:
                suggestion = guess_command(command, sub_command)
                if suggestion:
                    print(f"❓ Unknown command '{command} {sub_command or ''}'. Maybe you meant: '{suggestion}'?")
                else:
                    print("❗ Invalid command. Type 'help' to see available commands.")


    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user.")
    finally:
        print(f"✅ Contacts saved to {FILENAME}")
        print("👋 Good bye!")
        save_book(book)

if __name__ == "__main__":
    main()
