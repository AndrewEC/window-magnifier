from __future__ import annotations
from typing import Tuple, Dict
from threading import Lock, Thread
import time

import pygetwindow as gw

from arguments import Arguments
from countdown_latch import CountDownLatch


class WindowInfo:

    def __init__(self, size: Tuple[int, int], position: Tuple[int, int]):
        self.size = size
        self.position = position

    def get_size(self) -> Tuple[int, int]:
        return self.size

    def as_capture_bounds(self) -> Dict[str, int]:
        return {"top": self.position[1], "left": self.position[0], "width": self.size[0], "height": self.size[1]}

    def get_scaled_size(self, scale_up_by: float) -> Tuple[int, int]:
        size = self.get_size()
        return int(size[0] * scale_up_by), int(size[1] * scale_up_by)

    @staticmethod
    def default_window_info() -> WindowInfo:
        return WindowInfo((0, 0), (10, 10))

    def __eq__(self, other: WindowInfo) -> bool:
        return self.size[0] == other.size[0] and self.size[1] == other.size[1] and self.position[0] == other.position[0] and self.position[1] == self.position[1]


def get_core_window_info(arguments: Arguments) -> WindowInfo:
    try:
        window_title = arguments.target_window_title
        windows = gw.getWindowsWithTitle(window_title)
        desired_window = next((window for window in windows if window.title == window_title), None)
        if desired_window is None:
            return WindowInfo.default_window_info()

        position = desired_window.topleft
        size = desired_window.size

        return WindowInfo(size, position)
    except Exception:
        return WindowInfo.default_window_info()


def get_starting_window_info(arguments: Arguments) -> WindowInfoContainer:
    return WindowInfoContainer(get_core_window_info(arguments))


class WindowInfoContainer:

    def __init__(self, info: WindowInfo):
        self._info = info
        self._lock = Lock()

    def get_window_info(self) -> WindowInfo:
        with self._lock:
            return self._info

    def set_window_info(self, window_info: WindowInfo):
        with self._lock:
            self._info = window_info


class WindowLookupThread(Thread):

    def __init__(self, window_info_container: WindowInfoContainer, arguments: Arguments, latch: CountDownLatch):
        super().__init__()
        self._running = True
        self._arguments = arguments
        self._window_info_container = window_info_container
        self._window_info = self._window_info_container.get_window_info()
        self._latch = latch

    def run(self):
        print('Starting window lookup thread')
        while self._running:
            try:
                window_info = get_core_window_info(self._arguments)

                if window_info == WindowInfo.default_window_info():
                    self._window_info_container.set_window_info(window_info)
                    self.stop_running()
                    break

                if self._window_info != window_info:
                    self._window_info = window_info
                    self._window_info_container.set_window_info(window_info)
            except Exception:
                pass
            time.sleep(0.05)
        print('Window lookup thread ended.')
        self._latch.count_down()

    def stop_running(self):
        print('Window lookup thread stop requested.')
        self._running = False


def start_window_lookup_thread(window_info_container: WindowInfoContainer, arguments: Arguments,
                               latch: CountDownLatch) -> WindowLookupThread:
    window_lookup_thread = WindowLookupThread(window_info_container, arguments, latch)
    window_lookup_thread.start()
    return window_lookup_thread
