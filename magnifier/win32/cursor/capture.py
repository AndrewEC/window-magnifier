from typing import Tuple

import win32gui, win32ui
from PIL import Image


_last_cursor_image = None


def _get_cursor_size(hcursor) -> Tuple[int, int]:  # https://stackoverflow.com/a/67265511
    info = win32gui.GetIconInfo(hcursor)

    if info[4]:  # Icon has color plane.
        bmp = win32gui.GetObject(info[4])

        width = bmp.bmWidth
        height = bmp.bmHeight
    else:  # Icon has no colour plane, image data stored in mask.
        bmp = win32gui.GetObject(info[3])

        width = bmp.bmWidth
        height = bmp.bmHeight // 2  # A monochrome icon contains image and XOR mask in the hbmMask.

    return width, height


# Modified version of snippet from: https://github.com/BoboTiG/python-mss/issues/55#issuecomment-580481146
def get_cursor_image(hcursor) -> Image:
    global _last_cursor_image
    try:
        icon_size = _get_cursor_size(hcursor)

        wdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(wdc, icon_size[0], icon_size[1])
        hdc = wdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), hcursor)

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DestroyIcon(hcursor)
        win32gui.DeleteObject(hbmp.GetHandle())
        hdc.DeleteDC()
        wdc.DeleteDC()

        _last_cursor_image = image
        return image
    except Exception:
        return _last_cursor_image