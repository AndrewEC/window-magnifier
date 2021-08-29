from __future__ import annotations
import time

from magnifier.win32 import WindowInfo, WindowInfoContainer, get_core_window_info
from magnifier.util import Arguments

from .countdown_latch import CountDownLatch
from .base_thread import BaseThread


class WindowLookupThread(BaseThread):

    def __init__(self, window_info_container: WindowInfoContainer, arguments: Arguments, latch: CountDownLatch):
        super().__init__('WindowLookupThread', latch)
        self._arguments = arguments
        self._window_info_container = window_info_container
        self._window_info = self._window_info_container.get_window_info()

    def execute(self):
        try:
            window_info = get_core_window_info(self._arguments.target_window_title)

            if window_info.is_default_info():
                self._window_info_container.set_window_info(window_info)
                return

            if self._window_info != window_info:
                self._window_info = window_info
                self._window_info_container.set_window_info(window_info)
        except Exception:
            pass
        time.sleep(0.3)


def start_window_lookup_thread(window_info_container: WindowInfoContainer, arguments: Arguments,
                               latch: CountDownLatch) -> WindowLookupThread:
    window_lookup_thread = WindowLookupThread(window_info_container, arguments, latch)
    window_lookup_thread.start()
    return window_lookup_thread
