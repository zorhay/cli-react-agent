from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from src.cli.static import MENU_TEXT


class Menu:
    def __init__(self, console: Console):
        self.console = console

    def show(self):
        """Displays the main menu of the AI agent CLI."""
        menu_text = MENU_TEXT
        self.console.print(Panel(menu_text, title="Main Menu", border_style="green"))

    def get_choice(self) -> str:
        """Prompts the user for a choice from the menu."""
        return Prompt.ask(
            Text("Choose an option", style="bold"),
            choices=["1", "2", "3"],
            default="1"
        )
