from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def success(message: str):
    console.print(f":white_check_mark: [green]{message}[/]")

def error(message: str):
    console.print(f":x: [bold red]{message}[/]")

def warning(message: str):
    console.print(f":warning: [yellow]{message}[/]")

def info(message: str):
    console.print(f":information_source: [blue]{message}[/]")

def show_panel(title: str, content: str, style: str = "cyan"):
    console.print(Panel(content, title=title, style=style))

def show_markdown(md_text: str):
    console.print(Markdown(md_text))

def rule(title: str):
    console.rule(f"[bold blue]{title}[/]")
