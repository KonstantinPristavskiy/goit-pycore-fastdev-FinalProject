# guesser.py

import difflib

KNOWN_COMMANDS = [
    "add",
    "show",
    "delete",
    "add-phone",
    "remove-phone",
    "set-birthday",
    "remove-birthday",
    "birthdays",
    "set-address",
    "remove-address",
    "set-email",
    "remove-email",
    "all",
    "help",
    "exit",
    "close",
    "hello"
]

def guess_command(user_input: str) -> str | None:
    guess = difflib.get_close_matches(user_input, KNOWN_COMMANDS, n=1, cutoff=0.6)
    return guess[0] if guess else None
