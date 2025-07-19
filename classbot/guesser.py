import difflib

# Повний список дозволених команд
KNOWN_COMMANDS = [
    "contact set", "contact get", "contact delete",
    "note set", "note get", "note delete",
    "help", "exit", "close"
]

# Альтернативні назви команд (alias -> нормальна назва)
ALIASES = {
    "rm": "delete",
    "del": "delete",
    "add": "set",
    "create": "set",
    "show": "get",
    "view": "get",
    "leave": "exit",
    "quit": "exit",
}


def normalize(word: str | None) -> str:
    """
    Перетворює скорочення на повні команди.
    """
    if not word:
        return ""
    return ALIASES.get(word.lower(), word.lower())


def guess_command(command: str, sub_command: str | None = None, max_guesses: int = 3) -> list[str]:
    """
    Повертає список найбільш схожих команд.
    Підтримує alias, декілька варіантів і неповні команди.
    """
    command = normalize(command)
    sub_command = normalize(sub_command)

    # Формуємо комбінацію
    input_combo = f"{command} {sub_command}".strip()

    # Спроба знайти найбільш схожі варіанти
    guesses = difflib.get_close_matches(input_combo, KNOWN_COMMANDS, n=max_guesses, cutoff=0.5)
    return guesses
