import sys
from queue import Queue

from magnifier.util import Arguments, ScaleContainer
from magnifier.threads import start_conversion_thread, start_capture_thread, start_window_lookup_thread, CountDownLatch
from magnifier.win32 import get_starting_window_info
from .display_window import start_display_window


def start_magnifier(arguments: Arguments):
    window_info_container = get_starting_window_info(arguments.target_window_title)
    capture_queue = Queue()
    conversion_queue = Queue()
    latch = CountDownLatch(3)
    scale_container = ScaleContainer()

    capture_thread = start_capture_thread(capture_queue, window_info_container, arguments, latch)
    conversion_thread = start_conversion_thread(capture_queue, conversion_queue, window_info_container, scale_container,
                                                latch, arguments)
    window_lookup_thread = start_window_lookup_thread(window_info_container, arguments, latch)

    def stop_on_exit_requested():
        print('Exit requested, closing.')
        window_lookup_thread.request_stop()
        capture_thread.request_stop()
        conversion_thread.request_stop()

        latch.await_countdown()
        sys.exit(0)

    start_display_window(conversion_queue, window_info_container, scale_container, arguments,
                         stop_on_exit_requested)
