# guesser.py

import difflib

# Список команд з урахуванням ієрархії
KNOWN_COMMANDS = [
    "contact set", "contact get", "contact delete",
    "note set", "note delete", "note get",
    "help", "exit", "close"
]


def guess_command(command: str, sub_command: str | None) -> str | None:
    """
    Повертає найбільш схожу команду, якщо користувач зробив помилку.
    Підтримує як command, так і pair 'command sub_command'.
    """
    if command == "contact" and sub_command:
        input_combo = f"{command} {sub_command}"
    else:
        input_combo = command

    guess = difflib.get_close_matches(input_combo, KNOWN_COMMANDS, n=1, cutoff=0.6)
    return guess[0] if guess else None
