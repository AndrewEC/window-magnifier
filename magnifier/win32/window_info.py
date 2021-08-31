from __future__ import annotations
from typing import Tuple, Dict

import win32gui

from magnifier.util import invoke_and_suppress


def get_window_handle(window_title: str):
    return invoke_and_suppress(lambda: win32gui.FindWindow(None, window_title))


def get_window_info_by_handle(hwnd) -> WindowInfo:
    if hwnd is None:
        return WindowInfo.default_window_info()

    rect = win32gui.GetWindowRect(hwnd)

    position = (rect[0], rect[1])
    size = (rect[2] - position[0], rect[3] - position[1])

    return WindowInfo(size, position)


class WindowInfo:

    def __init__(self, size: Tuple[int, int], position: Tuple[int, int]):
        self.size = size
        self.position = position

    def as_capture_bounds(self) -> Dict[str, int]:
        return {"top": self.position[1], "left": self.position[0], "width": self.size[0], "height": self.size[1]}

    def is_default_info(self) -> bool:
        return WindowInfo.default_window_info() == self

    def __eq__(self, other: WindowInfo) -> bool:
        return self.size[0] == other.size[0] and self.size[1] == other.size[1] and self.position[0] == other.position[0] and self.position[1] == self.position[1]

    @staticmethod
    def default_window_info() -> WindowInfo:
        return WindowInfo((0, 0), (10, 10))
