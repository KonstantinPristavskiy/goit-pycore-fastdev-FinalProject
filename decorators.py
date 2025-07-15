def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "⚠️ Contact not found."
        except ValueError as e:
            return f"❌ {str(e)}"
        except IndexError:
            return "❌ Not enough arguments."
    return inner
