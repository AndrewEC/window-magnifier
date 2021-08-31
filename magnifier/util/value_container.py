from typing import TypeVar, Generic, Any

from threading import Lock


T = TypeVar('T')


class ValueContainer(Generic[T]):

    def __init__(self, initial_value: T = None):
        self._lock = Lock()
        self._value: T = initial_value

    def get_value(self) -> T:
        with self._lock:
            return self._value

    def set_value(self, value: T):
        with self._lock:
            self._value = value


class WindowHandleContainer(ValueContainer[Any]):

    def __init__(self, initial_value=None):
        super().__init__(initial_value)


class ScaleContainer(ValueContainer[float]):

    def __init__(self):
        super().__init__(1.0)
