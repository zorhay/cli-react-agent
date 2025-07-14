from typing import Callable

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from src.stream.parser import MessageType


class ChatSession:
    def __init__(self, console: Console, stream: Callable):
        self.console = console
        self.stream = stream

    def _get_user_massage(self):
        """
        Handles user message:
            shows in console panel
            exit the chat session if exit command provided
        :return: should chat continue or not
        """
        question = Prompt.ask("\n[bold]You[/bold]")
        if question.lower().strip() in ['exit', 'quit']:
            return False  # quit the session

        self.console.print(
            Panel(Text(question, justify="full"), title="[yellow]You[/yellow]", border_style="yellow", expand=False)
        )
        return question

    def _send_answer(self, answer: str):
        self.console.print(
            Panel(
                Text(answer, justify="full"), title="[bold cyan]Agent[/bold cyan]", border_style="blue", expand=False
            )
        )

    def _handle_progress(self, title: str, content: str):
        self.console.status(f"[bold green]{title}...[/bold green]")
        message = Text.from_markup(f"[bold green]{title}:[/bold green] ")
        message.append(Text(content, style="dim white"))
        self.console.log(message)

    async def _handle_single_prompt_cycle(self):
        question = self._get_user_massage()
        if not question:
            return False  # Signal to stop chat

        async for message in self.stream(question):
            if message.message_type in MessageType.in_progress_types():
                self._handle_progress(message.message_type.name, message.content)
            elif message.message_type == MessageType.FINAL_ANSWER:
                self._send_answer(message.content)
                break
            else:
                self.console.print("[bold red]Sorry, something went wrong![/red]")
        return True  # Signal to continue

    async def run(self):
        """
        Initializes and runs a continuous chat session loop.
        """
        self.console.print(Panel(
            """You are now in a chat session with the AI agent.\n
Type [bold red]exit[/bold red] or [bold red]quit[/bold red] to return to the main menu.""",
            title="Chat Session", border_style="magenta", expand=False))

        while True:
            should_continue = await self._handle_single_prompt_cycle()
            if not should_continue:
                break
