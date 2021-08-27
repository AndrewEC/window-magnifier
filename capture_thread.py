import threading
import time
from queue import Queue

import mss

from window_locator import WindowInfoContainer
from arguments import Arguments


class CaptureThread(threading.Thread):

    def __init__(self, capture_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments):
        super().__init__()
        self._capture_queue = capture_queue
        self._capture_screen = mss.mss()
        self._window_info = window_info_container
        self._running = True
        self._arguments = arguments

    def run(self):
        print('Starting capture thread')
        while self._running:
            capture_data = self._capture_screen.grab(self._window_info.get_window_info().as_capture_bounds())
            self._capture_queue.put(capture_data, True, timeout=0.1)
            time.sleep(0.01)
        print('Stopping capture thread')

    def stop_running(self):
        self._running = False


def start_capture_thread(capture_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments):
    capture_thread = CaptureThread(capture_queue, window_info_container, arguments)
    capture_thread.start()
    return capture_thread
