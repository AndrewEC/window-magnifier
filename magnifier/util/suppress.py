from typing import Callable


def invoke_and_suppress(func: Callable):
    try:
        return func()
    except Exception:
        return None
