import time
from queue import Queue

from magnifier.util import Arguments
from magnifier.win32 import add_cursor_to_image, capture_image_of_window

from .window_locator import WindowInfoContainer
from .countdown_latch import CountDownLatch
from .base_thread import BaseThread


class CaptureThread(BaseThread):

    def __init__(self, capture_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments,
                 latch: CountDownLatch):
        super().__init__('CaptureThread', latch)
        self._capture_queue = capture_queue
        self._window_info_container = window_info_container
        self._arguments = arguments

    def execute(self):
        try:
            window_info = self._window_info_container.get_window_info()

            if window_info.is_default_info():
                return

            captured_image = capture_image_of_window(window_info.window_handle)

            if self._arguments.capture_mouse:
                add_cursor_to_image(captured_image, window_info)

            self._capture_queue.put(captured_image, True, timeout=0.1)
        except Exception:
            time.sleep(0.5)
        time.sleep(self._arguments.capture_delay_interval)


def start_capture_thread(capture_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments,
                         latch: CountDownLatch):
    capture_thread = CaptureThread(capture_queue, window_info_container, arguments, latch)
    capture_thread.start()
    return capture_thread
