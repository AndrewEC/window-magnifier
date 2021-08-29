from PIL import Image

import win32gui
import win32ui
import win32con

from .window_position import get_core_window_info_by_hwnd


def capture_image_of_window(hwnd) -> Image:
    window_info = get_core_window_info_by_hwnd(hwnd)

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, window_info.size[0], window_info.size[1])

    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), window_info.size, dcObj, (0, 0), win32con.SRCCOPY)

    bmpstr = dataBitMap.GetBitmapBits(True)
    image = Image.frombuffer('RGB', window_info.size, bmpstr, 'raw', 'BGRX', 0, 1)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return image
