from classbot.storage import load_data, save_data, FILENAME
from classbot.handlers import (
    contact_set, contact_get, contact_delete, show_help, note_set,
    note_get, note_delete)
from classbot.notebook import NoteBook 
from classbot.guesser import guess_command
from classbot.address_book import AddressBook
from classbot.console import console, success, error, info, warning, show_panel, rule


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
    if command != 'contact' and command != 'note':
        return command, None, parts[1:]

    # Якщо команда 'contact', але немає підкоманди.
    if len(parts) < 2:
        return command, None, []

    sub_command = parts[1].lower()
    args = parts[2:]
    return command, sub_command, args

def main():
    data = load_data()  # Завантажуємо і контакти, і нотатки
    book = data.get('contacts', AddressBook())
    notebook = data.get('notes', NoteBook())

    # Словник для команд, що стосуються контактів
    contact_commands = {
        "set": contact_set,
        "get": contact_get, 
        "delete": contact_delete,
    }

    # Словник для команд, що стосуються нотаток
    note_commands = {
        "set": note_set,
        "get": note_get,
        "delete": note_delete,
    }
    rule("Welcome to CLASS CLI Assistant 🤖")
    info("Type 'help' to see available commands.\n")

    try:
        while True:
            user_input = console.input("📥 [bold cyan]Enter a command[/]: ")
            command, sub_command, args = parse_input(user_input)

            if not command:
                continue

            if command in ["close", "exit"]:
                success("Session ended. Goodbye!")
                break

            elif command == "help":
                show_panel("HELP", show_help())
            
            # Виклик обробників для команди 'contact'
            elif command == 'contact':
                if sub_command in contact_commands:
                    response = contact_commands[sub_command](args, book)
                    console.print(response)
                else:
                    suggestion = guess_command(command, sub_command)
                    if suggestion:
                        warning(f"Unknown subcommand '{sub_command}'. Did you mean '{suggestion}'?")
                    else:
                        error("Invalid contact command. Use: set, get, delete, or help.")
            
            # Виклик обробників для команди 'note'
            elif command == 'note':
                if sub_command in note_commands:
                    response = note_commands[sub_command](args, notebook)
                    console.print(response)
                else:
                    suggestion = guess_command(command, sub_command)
                    if suggestion:
                        warning(f"Unknown subcommand '{sub_command}'. Did you mean '{suggestion}'?")
                    else:
                        error("Invalid note command. Use: set, get, delete, or help.")

            
            else:
                suggestion = guess_command(command, sub_command)
                if suggestion:
                    warning(f"Unknown command '{command} {sub_command or ''}'. Did you mean '{suggestion}'?")
                else:
                    error("Unknown command. Type 'help' to see available commands.")


    except KeyboardInterrupt:
        warning("\nProgram interrupted by user (Ctrl+C).")

    finally:
        save_data({'contacts': book, 'notes': notebook})
        success(f"All data saved to [bold]{FILENAME}[/].")
        rule("Goodbye 👋")

if __name__ == "__main__":
    main()
