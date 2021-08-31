from typing import Tuple

import win32gui, win32ui
from PIL import Image

from magnifier.win32 import WindowInfo


MOUSE_HIDDEN_FLAG = 0
DEFAULT_MOUSE_PIXEL_COLOUR = 10
COLOURS_PER_PIXEL = 3


last_cursor_image = None


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
def _get_cursor_image(hcursor) -> Image:
    global last_cursor_image
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

        last_cursor_image = image
        return image
    except Exception as e:
        print(str(e))
        return last_cursor_image


def _should_copy_pixel(colour: Tuple[int, int, int]) -> bool:
    return colour[0] > 0 and colour[1] > 0 and colour[2] > 0


def _is_position_within_rect(position: Tuple[int, int], rect: Tuple[int, int, int, int]):
    return rect[0] < position[0] < rect[0] + rect[2] and rect[1] < position[1] < rect[1] + rect[3]


def _is_mouse_over_target_application(x: int, y: int, window_info: WindowInfo) -> bool:
    size = window_info.size
    position = window_info.position
    return _is_position_within_rect((x, y), (position[0], position[1], size[0], size[1]))


def _is_pixel_within_image_bounds(x: int, y: int, image: Image) -> bool:
    return _is_position_within_rect((x, y), (0, 0, image.size[0], image.size[1]))


def _paste_cursor_on_image(cursor_x: int, cursor_y: int, cursor_image: Image, captured_image: Image,
                           window_info: WindowInfo):
    size = cursor_image.size
    pixel_data = cursor_image.load()
    for source_pixel_x in range(size[0]):
        for source_pixel_y in range(size[1]):
            pixel = pixel_data[source_pixel_x, source_pixel_y]

            if not _should_copy_pixel(pixel):
                continue

            x = source_pixel_x + cursor_x - window_info.position[0]
            y = source_pixel_y + cursor_y - window_info.position[1]
            if not _is_pixel_within_image_bounds(x, y, captured_image):
                continue
            captured_image.putpixel((x, y), (DEFAULT_MOUSE_PIXEL_COLOUR,) * COLOURS_PER_PIXEL)


def add_cursor_to_image(captured_image: Image, window_info: WindowInfo):
    flags, hcursor, (cursor_x, cursor_y) = win32gui.GetCursorInfo()

    if flags == MOUSE_HIDDEN_FLAG:
        return

    if not _is_mouse_over_target_application(cursor_x, cursor_y, window_info):
        return

    cursor_image = _get_cursor_image(hcursor)
    _paste_cursor_on_image(cursor_x, cursor_y, cursor_image, captured_image, window_info)
