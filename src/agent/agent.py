from typing import List, Tuple

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.store.base import BaseStore
from langchain.chat_models import init_chat_model
from langchain_core.tools import BaseTool
from langchain_core.messages import SystemMessage
from pydantic import BaseModel

from src.agent.prompt import SYSTEM_PROMPT
from src.agent.store import get_store_with_embeddings
from src.agent.tools import tools as default_tools
from src.agent.tools.store_wrapper import StoreInteractionToolWrapper
from src.config import AgentSettings


class ResponseFormat(BaseModel):
    final_answer: str


def _initialize_model(settings: AgentSettings):
    """Initializes the chat model based on the provided settings."""
    return init_chat_model(
        model=settings.intelligence_model,
        model_provider=settings.provider,
        temperature=settings.temperature
    )


def _initialize_tools(settings: AgentSettings) -> Tuple[List[BaseTool], BaseStore]:
    """Initializes and returns the list of tools for the agent and the data store."""
    store = get_store_with_embeddings(settings.embedding_model)
    store_tools = StoreInteractionToolWrapper(store=store).get_tools()
    return default_tools + store_tools, store


def init_agent(settings: AgentSettings):
    """Initializes and configures the ReAct agent."""
    model = _initialize_model(settings)
    all_tools, store = _initialize_tools(settings)
    memory = InMemorySaver()

    agent = create_react_agent(
        model=model,
        tools=all_tools,
        prompt=SystemMessage(content=SYSTEM_PROMPT),
        checkpointer=memory,
        response_format=ResponseFormat
    ).with_config(thread_id=settings.thread_id)
    # The store is attached to the tools, but we attach it to the agent instance
    # for convenience so it can be accessed directly, e.g. for populating data.
    agent.store = store
    return agent
