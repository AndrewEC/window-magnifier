from abc import abstractmethod
from threading import Thread, Event

from .countdown_latch import CountDownLatch


class BaseThread(Thread):

    def __init__(self, name: str, latch: CountDownLatch):
        super().__init__()
        self._latch = latch
        self._stop_event = Event()
        self._name = name

    def run(self):
        print(f'Starting thread: [{self._name}]')
        while not self._stop_event.is_set():
            self.execute()
        print(f'Stopping thread: [{self._name}]')
        self._latch.count_down()

    @abstractmethod
    def execute(self):
        pass

    def request_stop(self):
        print(f'Request to stop thread [{self._name}] received.')
        self._stop_event.set()
