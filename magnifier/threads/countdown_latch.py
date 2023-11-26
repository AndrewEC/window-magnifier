from threading import Condition


class CountDownLatch:

    def __init__(self, count: int):
        self._condition = Condition()
        self._count = count

    def count_down(self):
        with self._condition:
            self._count = self._count - 1
            if self._count == 0:
                self._condition.notify_all()

    def await_countdown(self):
        with self._condition:
            while self._count > 0:
                self._condition.wait()
