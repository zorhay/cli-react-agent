import requests
from bs4 import BeautifulSoup


def read_web_page(url: str) -> str:
    """
    Reads the textual content of a web page from a given URL.
    Useful for parsing the content from archive.org

    Args:
        url: The URL of the web page to read.

    Returns:
        The extracted text from the web page, or an error message if the page cannot be fetched or parsed.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' # noqa: E501
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get text and clean up whitespace
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text or "Error: Could not extract any text from the page."
    except requests.exceptions.RequestException as e:
        return f"Error: Could not fetch the web page. {e}"
    except Exception as e:
        return f"An unexpected error occurred while reading the web page: {e}" 