from enum import Enum, auto
from typing import AsyncGenerator, Callable

from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, ToolMessage
from pydantic import BaseModel


class Message(BaseModel):
    messages: list[dict[str, str]]


class MessageType(Enum):
    """Enumeration for the agent's ReAct states."""
    USER = auto()
    THOUGHT = auto()
    ACTION = auto()
    OBSERVATION = auto()
    FINAL_ANSWER = auto()

    @classmethod
    def in_progress_types(cls):
        return [cls.THOUGHT, cls.ACTION, cls.OBSERVATION]


class ParserMessage(BaseModel):
    message_type: MessageType
    content: str


def parse_message(message: BaseMessage) -> list[ParserMessage]:
    """Parses a message from the agent into a list of ParserMessage objects."""
    parsed_messages = []

    if isinstance(message, HumanMessage):
        parsed_messages.append(ParserMessage(message_type=MessageType.USER, content=message.content))
    elif isinstance(message, AIMessage):
        # An AIMessage can contain both a thought (content) and actions (tool_calls).
        if message.content:
            content = "\n".join(message.content) if isinstance(message.content, list) else message.content
            parsed_messages.append(ParserMessage(message_type=MessageType.THOUGHT, content=content))
        for tool_call in message.tool_calls:
            tool_content = f"{tool_call['name']}: {tool_call['args']}"
            parsed_messages.append(ParserMessage(message_type=MessageType.ACTION, content=tool_content))
    elif isinstance(message, ToolMessage):
        parsed_messages.append(ParserMessage(message_type=MessageType.OBSERVATION, content=str(message.content)))
    else:
        # This provides a fallback for any unexpected message types.
        parsed_messages.append(ParserMessage(message_type=MessageType.OBSERVATION, content=str(message)))

    return parsed_messages


def console_agent_stream_wrapper(agent) -> Callable[[str], AsyncGenerator[ParserMessage, None]]:
    async def wrapped(input_message: str):
        message = Message(messages=[{"role": "user", "content": input_message}])
        async for step in agent.astream(message, stream_mode="updates"):
            if "generate_structured_response" in step and "structured_response" in step["generate_structured_response"]:
                final_answer = step["generate_structured_response"]["structured_response"].final_answer
                yield ParserMessage(message_type=MessageType.FINAL_ANSWER, content=final_answer)
                break

            messages = step.get("agent", {}) or step.get("tools", {})
            if not messages or "messages" not in messages:
                continue

            response = messages["messages"][-1]
            response_parsed = parse_message(response)
            for parsed in response_parsed:
                yield parsed
    return wrapped
