from __future__ import annotations
from typing import Tuple, Optional

import ctypes
from ctypes import wintypes

import win32gui

from magnifier.util import invoke_and_suppress


# https://stackoverflow.com/questions/51786794/using-imagegrab-with-bbox-from-pywin32s-getwindowrect
ctypes.windll.user32.SetProcessDPIAware()


DWMWA_EXTENDED_FRAME_BOUNDS = 9


def get_window_handle(window_title: str):
    return invoke_and_suppress(lambda: win32gui.FindWindow(None, window_title))


def _diff(num1: int, num2: int) -> int:
    return abs(abs(num1) - abs(num2))


def get_window_info(hwnd) -> WindowInfo:
    window_info_with_decor = _get_window_info_with_decor(hwnd)
    window_info_without_decor = _get_window_info_without_decor(hwnd)

    screen_position = win32gui.ClientToScreen(hwnd, (0, 0))

    title_bar_height = _diff(screen_position[1], window_info_without_decor.position[1])
    size = (window_info_without_decor.size[0], window_info_without_decor.size[1] - title_bar_height)

    return WindowInfo(size, screen_position, window_info_with_decor)


def _get_window_info_with_decor(hwnd) -> Optional[WindowInfo]:
    if hwnd is None:
        return None

    rect = win32gui.GetWindowRect(hwnd)

    position = (rect[0], rect[1])
    size = (rect[2] - position[0], rect[3] - position[1])

    return WindowInfo(size, position)


def _get_window_info_without_decor(hwnd) -> Optional[WindowInfo]:
    if hwnd is None:
        return None

    rect = ctypes.wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(ctypes.wintypes.HWND(hwnd),
                                               ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
                                               ctypes.byref(rect),
                                               ctypes.sizeof(rect))

    position = (rect.left, rect.top)
    size = (rect.right - rect.left, rect.bottom - rect.top)

    return WindowInfo(size, position)


class WindowInfo:

    def __init__(self, size: Tuple[int, int], position: Tuple[int, int], with_decorations: WindowInfo = None):
        self.size = size
        self.position = position
        self.with_decorations = with_decorations

    def __eq__(self, other: WindowInfo) -> bool:
        return self.size[0] == other.size[0] and self.size[1] == other.size[1] and self.position[0] == other.position[0] and self.position[1] == self.position[1]
