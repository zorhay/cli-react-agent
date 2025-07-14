from typing import Any, List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langgraph.store.base import BaseStore


class PutInput(BaseModel):
    namespace: List[str] = Field(..., description="""
    The namespace to write to, as a list of two strings. Example: ['user_id', 'memories']
    """)
    key: str = Field(..., description="The unique key for the value.")
    value: dict = Field(..., description="The value to store.")


class GetInput(BaseModel):
    namespace: List[str] = Field(..., description="""
    The namespace to read from, as a list of two strings. Example: ['user_id', 'memories']
    """)
    key: str = Field(..., description="The key of the value to retrieve.")


class SearchInput(BaseModel):
    namespace_prefix: List[str] = Field(..., description="""
    The namespace to search within, as a list of two strings. Example: ['user_id', 'memories']
    """)
    query: str = Field(..., description="The query to search for.")
    limit: Optional[int] = Field(4, description="The number of results to return.")


class ListNamespacesInput(BaseModel):
    prefix: Optional[List[str]] = Field(None, description="""
    A prefix to filter namespaces, as a list of two strings. Example: ['user_id', 'memories']
    """)


class StoreInteractionToolWrapper:
    """ Allows an agent to interact with the store."""
    def __init__(self, store: BaseStore):
        self.store = store

    def put(self, namespace: List[str], key: str, value: dict) -> None:
        """
        Stores a key-value pair in a specific namespace. Use this to remember information, facts, or user preferences
        for later retrieval. For example, you can store a user's favorite movie in the 'memories' namespace.
        The namespace should be a list of two strings, like ['user_id', 'memories'].
        """
        return self.store.put(namespace=tuple(namespace), key=key, value=value)

    def search(self, namespace_prefix: List[str], query: str, limit: int = 4) -> List[Any]:
        """
        Searches for relevant information within a given namespace based on a natural language query.
        This is useful for finding stored facts or memories. For example, searching for 'Pulp Fiction' in the
        'memories' namespace would return related stored information. The namespace_prefix must be a list of
        strings, like ['user_id', 'memories'].
        """
        # Call with namespace_prefix as a positional argument, not a keyword one.
        return self.store.search(tuple(namespace_prefix), query=query, limit=limit)

    def get(self, namespace: List[str], key: str) -> Any:
        """
        Retrieves a specific value from a namespace using its exact key. Use this when you know the precise key
        of the information you need. The namespace must be a list of two strings, like ['user_id', 'memories'].
        """
        return self.store.get(namespace=tuple(namespace), key=key)

    def list_namespaces(self, prefix: Optional[List[str]] = None) -> list[tuple[str, ...]]:
        """
        Lists all available namespaces in the store. This is useful to understand the overall data structure
        and see where information is organized. You can optionally provide a prefix to filter the results,
        for example, ['user_id'] to see all namespaces for a specific user.
        """
        namespace_tuple = None if prefix is None else tuple(prefix)
        return self.store.list_namespaces(prefix=namespace_tuple)

    def get_tools(self):
        """Returns the store methods as a list of tools for the agent."""
        put_tool = tool(self.put, args_schema=PutInput)
        get_tool = tool(self.get, args_schema=GetInput)
        search_tool = tool(self.search, args_schema=SearchInput)
        list_tool = tool(self.list_namespaces, args_schema=ListNamespacesInput)

        return [put_tool, get_tool, search_tool, list_tool]
