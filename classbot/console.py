from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def success(message: str):
    formatted = f":white_check_mark: [green]{message}[/]"
    console.print(formatted)
    return ""  # Повертаємо порожній рядок замість None

def error(message: str):
    formatted = f":x: [bold red]{message}[/]"
    console.print(formatted)
    return ""

def warning(message: str):
    formatted = f":warning: [yellow]{message}[/]"
    console.print(formatted)
    return ""

def info(message: str):
    formatted = f":information_source: [blue]{message}[/]"
    console.print(formatted)
    return ""

def show_panel(title: str, content: str, style: str = "cyan"):
    console.print(Panel(content, title=title, style=style))

def show_markdown(md_text: str):
    console.print(Markdown(md_text))

def rule(title: str):
    console.rule(f"[bold blue]{title}[/]")
