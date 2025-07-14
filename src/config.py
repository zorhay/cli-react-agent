"""Configuration for the AI agent."""
import uuid
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # loads API keys


class AgentSettings(BaseSettings):
    provider: str = "google_genai"
    intelligence_model: str = "gemini-2.5-pro"
    embedding_model: str = "models/text-embedding-004"
    temperature: float = 0.0
    thread_id: str = Field(default_factory=lambda: f"thread-{uuid.uuid4()}")


agent_settings = AgentSettings()
