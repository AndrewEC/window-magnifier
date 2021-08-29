from __future__ import annotations
from typing import Tuple, Dict
from threading import Lock

import win32gui


def get_core_window_info(window_title: str) -> WindowInfo:
    try:
        hwnd = win32gui.FindWindow(None, window_title)
        return get_core_window_info_by_hwnd(hwnd)
    except Exception:
        return WindowInfo.default_window_info()


def get_core_window_info_by_hwnd(hwnd) -> WindowInfo:
    if hwnd is None:
        return WindowInfo.default_window_info()

    rect = win32gui.GetWindowRect(hwnd)

    position = (rect[0], rect[1])
    size = (rect[2] - position[0], rect[3] - position[1])

    return WindowInfo(size, position, hwnd)


def get_starting_window_info(window_title: str) -> WindowInfoContainer:
    return WindowInfoContainer(get_core_window_info(window_title))


class WindowInfo:

    def __init__(self, size: Tuple[int, int], position: Tuple[int, int], handle=None):
        self.size = size
        self.position = position
        self.window_handle = handle

    def as_capture_bounds(self) -> Dict[str, int]:
        return {"top": self.position[1], "left": self.position[0], "width": self.size[0], "height": self.size[1]}

    def is_default_info(self) -> bool:
        return WindowInfo.default_window_info() == self

    def __eq__(self, other: WindowInfo) -> bool:
        return self.size[0] == other.size[0] and self.size[1] == other.size[1] and self.position[0] == other.position[0] and self.position[1] == self.position[1]

    @staticmethod
    def default_window_info() -> WindowInfo:
        return WindowInfo((0, 0), (10, 10))


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