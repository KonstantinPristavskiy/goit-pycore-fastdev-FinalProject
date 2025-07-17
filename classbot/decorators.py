from classbot.console import info, error

def input_error(func):
    """
    Декоратор для обробки помилок вводу, таких як KeyError, ValueError, IndexError.
    Повертає відповідне повідомлення про помилку.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return info("⚠️ Contact not found.")
        except ValueError as e:
            return error(f"❌ {str(e)}")
        except IndexError:
            return error("❌ Not enough arguments.")
    return inner
