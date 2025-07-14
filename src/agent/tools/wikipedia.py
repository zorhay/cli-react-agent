import wikipedia


def search_wikipedia(query: str) -> str:
    """
    Searches Wikipedia for a given query and returns a summary of the top result.
    Useful for looking up well established concepts, terms, geographical places and historical events

    Args:
        query: The search query.

    Returns:
        A summary of the top Wikipedia article, or an error message if no article was found.
    """
    try:
        # Get the summary of the first result
        summary = wikipedia.summary(query, sentences=5)
        return summary
    except wikipedia.exceptions.PageError:
        return f"Error: Could not find a Wikipedia page for '{query}'."
    except wikipedia.exceptions.DisambiguationError as e:
        # In case of a disambiguation page, return the options
        options = ", ".join(e.options[:5])
        return f"Error: '{query}' is ambiguous. Did you mean one of these: {options}?"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
