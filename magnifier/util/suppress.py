from typing import Callable, TypeVar, Optional


T = TypeVar('T')


def invoke_and_suppress(func: Callable[[], T]) -> Optional[T]:
    try:
        return func()
    except:
        return None
