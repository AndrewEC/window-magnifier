import threading
import time
from queue import Queue

import mss

from window_locator import WindowInfoContainer, WindowInfo
from arguments import Arguments
from countdown_latch import CountDownLatch


class CaptureThread(threading.Thread):

    def __init__(self, capture_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments,
                 latch: CountDownLatch):
        super().__init__()
        self._capture_queue = capture_queue
        self._capture_screen = mss.mss()
        self._window_info_container = window_info_container
        self._running = True
        self._arguments = arguments
        self._latch = latch

    def run(self):
        print('Starting capture thread')
        while self._running:
            try:
                window_info = self._window_info_container.get_window_info()

                if window_info == WindowInfo.default_window_info():
                    self.stop_running()
                    break

                capture_data = self._capture_screen.grab(window_info.as_capture_bounds())
                self._capture_queue.put(capture_data, True, timeout=0.1)
            except Exception:
                pass
            time.sleep(self._arguments.capture_delay_interval)
        print('Capture thread stopped.')
        self._latch.count_down()

    def stop_running(self):
        print('Capture thread stop requested.')
        self._running = False


def start_capture_thread(capture_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments,
                         latch: CountDownLatch):
    capture_thread = CaptureThread(capture_queue, window_info_container, arguments, latch)
    capture_thread.start()
    return capture_thread
