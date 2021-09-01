import time
from queue import Queue

from magnifier.util import Arguments, WindowHandleContainer
from magnifier.win32 import add_cursor_to_image, capture_image_of_window, get_window_info

from .countdown_latch import CountDownLatch
from .base_thread import BaseThread


class CaptureThread(BaseThread):

    def __init__(self, capture_queue: Queue, window_handle_container: WindowHandleContainer, arguments: Arguments,
                 latch: CountDownLatch):
        super().__init__('CaptureThread', latch)
        self._capture_queue = capture_queue
        self._arguments = arguments
        self._window_handle = window_handle_container.get_value()
        self._window_handle_container = window_handle_container

    def execute(self):
        try:
            window_info = get_window_info(self._window_handle)
            captured_image = capture_image_of_window(self._window_handle, window_info)

            if self._arguments.capture_mouse:
                add_cursor_to_image(captured_image, window_info)

            self._capture_queue.put(captured_image, True, timeout=0.1)
        except Exception as e:
            print(str(e))
            time.sleep(0.5)
            self._window_handle = self._window_handle_container.get_value()
        time.sleep(self._arguments.capture_delay_interval)


def start_capture_thread(capture_queue: Queue, window_handle_container: WindowHandleContainer, arguments: Arguments,
                         latch: CountDownLatch):
    capture_thread = CaptureThread(capture_queue, window_handle_container, arguments, latch)
    capture_thread.start()
    return capture_thread
