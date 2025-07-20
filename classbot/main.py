import shlex
from classbot.storage import load_data, save_data, FILENAME
from classbot.handlers import (
    contact_set, contact_get, contact_delete, show_help, note_set,
    note_get, note_delete)
from classbot.notebook import NoteBook 
from classbot.guesser import guess_command
from classbot.address_book import AddressBook
from classbot.console import console, success, error, info, warning, show_panel, rule
from rich.panel import Panel


def parse_input(user_input):
    """
    Розбирає введений рядок на основну команду, підкоманду та аргументи.
    Підтримує лапки для групування аргументів.
    """
    stripped = user_input.strip()
    if not stripped:
        return None, None, []
    
    try:
        parts = shlex.split(stripped)
    except ValueError:
        parts = stripped.split()
    
    command = parts[0].lower()
    if command not in ('contact', 'note'):
        return command, None, parts[1:]

    if len(parts) < 2:
        return command, None, []

    sub_command = parts[1].lower()
    args = parts[2:]
    return command, sub_command, args


def show_suggestions(entered_command, suggestions):
    """
    Виводить панель з підказками команд у форматі rich.
    """
    panel_text = f"[bold red]Unknown command:[/] [yellow]{entered_command}[/]\n\n"
    panel_text += "[green]Did you mean:[/]\n"
    for s in suggestions:
        panel_text += f"  • [bold cyan]{s}[/]\n"

    console.print(Panel(panel_text, title="Suggestions", border_style="red"))


def main():
    data = load_data()
    book = data.get('contacts', AddressBook())
    notebook = data.get('notes', NoteBook())

    contact_commands = {
        "set": contact_set,
        "get": contact_get, 
        "delete": contact_delete,
    }

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

            elif command == "contact":
                if sub_command in contact_commands:
                    response = contact_commands[sub_command](args, book)
                    if response:
                        console.print(response)
                else:
                    suggestions = guess_command(command, sub_command)
                    if suggestions:
                        show_suggestions(f"{command} {sub_command}", suggestions)
                    else:
                        error("Invalid contact command. Use: set, get, delete, or help.")

            elif command == "note":
                if sub_command in note_commands:
                    response = note_commands[sub_command](args, notebook)
                    if response:
                        console.print(response)
                else:
                    suggestions = guess_command(command, sub_command)
                    if suggestions:
                        show_suggestions(f"{command} {sub_command}", suggestions)
                    else:
                        error("Invalid note command. Use: set, get, delete, or help.")

            else:
                suggestions = guess_command(command, sub_command)
                if suggestions:
                    show_suggestions(command, suggestions)
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
