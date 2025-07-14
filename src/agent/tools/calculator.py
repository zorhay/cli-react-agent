import numexpr


def calculate(expression: str) -> str:
    """
    Evaluates a mathematical expression safely.
    Useful for not relying on models math capabilities.
    """
    try:
        result = numexpr.evaluate(expression)
        return str(result)
    except Exception as e:
        return f"Error: Invalid expression - {e}"
