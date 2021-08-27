import sys
from queue import Queue

from arguments import Arguments
from capture_thread import start_capture_thread
from conversion_thread import start_conversion_thread
from display_window import start_display_window
from window_locator import get_starting_window_info, start_window_lookup_thread
from countdown_latch import CountDownLatch


def start_magnifier(arguments: Arguments):
    window_info_container = get_starting_window_info(arguments)
    capture_queue = Queue()
    conversion_queue = Queue()

    latch = CountDownLatch(3)

    capture_thread = start_capture_thread(capture_queue, window_info_container, arguments, latch)
    conversion_thread = start_conversion_thread(capture_queue, conversion_queue, window_info_container, arguments, latch)
    window_lookup_thread = start_window_lookup_thread(window_info_container, arguments, latch)

    def stop_on_exit_requested():
        print('Exit requested, closing.')
        capture_thread.stop_running()
        conversion_thread.stop_running()
        window_lookup_thread.stop_running()

        latch.await_countdown()
        sys.exit(0)

    start_display_window(conversion_queue, window_info_container, arguments, stop_on_exit_requested)
