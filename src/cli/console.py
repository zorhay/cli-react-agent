import os
from typing import Callable

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from src.cli.chat_session import ChatSession
from src.cli.menu import Menu


class ConsoleApp:
    """
    An interactive CLI application for an AI agent, structured within a class.
    """

    def __init__(self, stream: Callable):
        """Initializes the console and the AI agent."""
        self.console = Console()
        self.stream = stream
        self.menu = Menu(self.console)

    def _clear_screen(self):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    async def show_chat_history(self):
        """Placeholder for showing chat history."""
        self._clear_screen()
        self.console.print(
            Panel("[bold yellow]Chat history feature is not yet implemented.[/bold yellow]", title="Coming Soon",
                  border_style="red"))
        Prompt.ask("\n[bold]Press Enter to return to the menu[/bold]")

    async def run(self):
        """The main entry point to run the interactive CLI."""
        while True:
            self._clear_screen()
            self.menu.show()
            choice = self.menu.get_choice()

            if choice == "1":
                chat_session = ChatSession(self.console, self.stream)
                await chat_session.run()
            elif choice == "2":
                await self.show_chat_history()
            elif choice == "3":
                self.console.print("[bold red]Deactivating agent. Goodbye![/bold red]")
                break
