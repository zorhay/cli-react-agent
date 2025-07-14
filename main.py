import asyncio
import uuid

from src.config import agent_settings
from src.cli.console import ConsoleApp
from src.agent import init_agent
from src.stream import console_agent_stream_wrapper


agent = init_agent(agent_settings)
stream_wrapper = console_agent_stream_wrapper(agent=agent)
console_app = ConsoleApp(stream=stream_wrapper)

if __name__ == "__main__":
    # init some data to the agent store
    for to_put in [
        (("1", "memories"), str(uuid.uuid4()), {"movie_preference": "Pulp Fiction is good one"}),
        (("1", "memories"), str(uuid.uuid4()), {"movie_preference": "2001: A Space Odyssey is very epic"}),
        (("1", "memories"), str(uuid.uuid4()), {"movie_preference": "Jackie Chan has funny roles"}),
        (("1", "memories"), str(uuid.uuid4()), {"movie_preference": "Iranian movies are non ordinary"})
    ]:
        agent.store.put(namespace=to_put[0], key=to_put[1], value=to_put[2])

    try:
        asyncio.run(console_app.run())
    except KeyboardInterrupt:
        print("\n[bold red]Application interrupted by user. Exiting...[/bold red]")
