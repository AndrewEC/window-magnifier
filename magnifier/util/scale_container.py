from threading import Lock


class ScaleContainer:

    def __init__(self):
        self._scale = 1.0
        self._lock = Lock()

    def get_scale(self) -> float:
        with self._lock:
            return self._scale

    def set_scale(self, size: float):
        with self._lock:
            self._scale = size
