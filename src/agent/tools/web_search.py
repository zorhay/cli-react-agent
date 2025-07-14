from langchain_tavily import TavilySearch
from typing import Dict, List


def search_web(query: str) -> Dict[str, List[str]]:
    """
    Performs a web search using the Tavily search engine.

    Args:
        query: The search query.

    Returns:
        A dictionary containing the search results.
    """
    result = TavilySearch().run(query)
    return result
