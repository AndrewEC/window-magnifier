import sys
from queue import Queue

from magnifier.win32 import get_window_handle
from magnifier.util import Arguments, ScaleContainer, WindowHandleContainer
from magnifier.threads import start_resize_thread, start_capture_thread, CountDownLatch
from .display_window import start_display_window


def start_magnifier(arguments: Arguments):
    window_handle_container = WindowHandleContainer(get_window_handle(arguments.target_window_title))
    scale_container = ScaleContainer()
    capture_queue = Queue()
    conversion_queue = Queue()
    latch = CountDownLatch(2)

    capture_thread = start_capture_thread(capture_queue, window_handle_container, arguments, latch)
    resize_thread = start_resize_thread(capture_queue, conversion_queue, window_handle_container,
                                        scale_container, latch, arguments)

    def stop_on_exit_requested():
        print('Exit requested, closing.')
        capture_thread.request_stop()
        resize_thread.request_stop()

        latch.await_countdown()
        sys.exit(0)

    start_display_window(conversion_queue, window_handle_container, scale_container, arguments,
                         stop_on_exit_requested)
