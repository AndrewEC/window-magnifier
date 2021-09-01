from typing import Tuple

from PIL import Image
from mss import mss

import win32gui
import win32ui
import win32con

from .window_info import WindowInfo


def _compute_crop_rect(window_info: WindowInfo) -> Tuple:
    left = window_info.position[0] - window_info.with_decorations.position[0]
    top = window_info.position[1] - window_info.with_decorations.position[1]
    right = left + window_info.size[0]
    bottom = top + window_info.size[1]
    return left, top, right, bottom


def _capture_painted_window(hwnd, window_info: WindowInfo) -> Image:
    size = window_info.with_decorations.size

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, size[0], size[1])

    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), size, dcObj, (0, 0), win32con.SRCCOPY)

    bmpstr = dataBitMap.GetBitmapBits(True)
    image = Image.frombuffer('RGB', size, bmpstr, 'raw', 'BGRX', 0, 1)
    crop_rect = _compute_crop_rect(window_info)
    image = image.crop(crop_rect)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return image


def _capture_screen_occupied_by_window(hwnd, window_info: WindowInfo) -> Image:
    box = {'top': window_info.position[1], 'left': window_info.position[0], 'width': window_info.size[0], 'height': window_info.size[1]}
    with mss() as screen:
        capture = screen.grab(box)
        return Image.frombytes('RGB', capture.size, capture.bgra, 'raw', 'BGRX')


def capture_image_of_window(screen_capture_mode: bool, hwnd, window_info: WindowInfo) -> Image:
    if screen_capture_mode:
        return _capture_screen_occupied_by_window(hwnd, window_info)
    else:
        return _capture_painted_window(hwnd, window_info)
