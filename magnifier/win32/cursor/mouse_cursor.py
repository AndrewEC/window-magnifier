from typing import Tuple, Callable

import win32gui
from PIL import Image

from magnifier.win32 import WindowInfo
from . import bounds
from . import capture


_MOUSE_HIDDEN_FLAG = 0
_COLOUR_WHITE = 255
_COLOUR_BLACK = 0
_COLOURS_PER_PIXEL = 3

_ADJACENT_PIXEL_MODIFIERS = [
    (-1, -1),
    (0, -1),
    (1, -1),

    (-1, 0),
    (1, 0),

    (-1, 1),
    (0, 1),
    (1, 1),
]


def _is_white_pixel(colour: Tuple[int, int, int]) -> bool:
    return colour[0] > 0 and colour[1] > 0 and colour[2] > 0


def _add_tuples(first: Tuple[int, int], second: Tuple[int, int]) -> Tuple[int, int]:
    return first[0] + second[0], first[1] + second[1]


def _is_pixel_from_cursor_image_white(pixel_position: Tuple[int, int], cursor_image: Image, cursor_image_pixel_data) -> bool:
    return bounds.is_position_within_image_bounds(*pixel_position, cursor_image) \
           and _is_white_pixel(cursor_image_pixel_data[pixel_position[0], pixel_position[1]])


def _add_border_pixels(source_pixel_position: Tuple[int, int],
                       destination_pixel_position: Tuple[int, int],
                       cursor_image_pixel_data,
                       captured_image: Image,
                       cursor_image: Image):

    # check that the pixel, pulled from the cursor image we are currently inspecting, is fully white in colour.
    if not _is_white_pixel(cursor_image_pixel_data[source_pixel_position[0], source_pixel_position[1]]):
        return

    for adjacent_modifier in _ADJACENT_PIXEL_MODIFIERS:

        adjacent_destination_position = _add_tuples(destination_pixel_position, adjacent_modifier)
        if not bounds.is_position_within_image_bounds(*adjacent_destination_position, captured_image):
            continue

        adjacent_source_position = _add_tuples(source_pixel_position, adjacent_modifier)
        if _is_pixel_from_cursor_image_white(adjacent_source_position, cursor_image, cursor_image_pixel_data):
            continue

        captured_image.putpixel(adjacent_destination_position, (_COLOUR_BLACK,) * _COLOURS_PER_PIXEL)


def _iterate_through_cursor_pixels(cursor_position: Tuple[int, int],
                                   cursor_image: Image,
                                   cursor_image_pixel_data,
                                   captured_image: Image,
                                   window_info: WindowInfo,
                                   callback: Callable[[Tuple[int, int, int], Tuple[int, int], Tuple[int, int]], None]):
    size = cursor_image.size
    for cursor_image_pixel_x in range(size[0]):
        for cursor_image_pixel_y in range(size[1]):
            pixel = cursor_image_pixel_data[cursor_image_pixel_x, cursor_image_pixel_y]
            mouse_relative_to_image_x = cursor_image_pixel_x + cursor_position[0] - window_info.position[0]
            mouse_relative_to_image_y = cursor_image_pixel_y + cursor_position[1] - window_info.position[1]
            if not bounds.is_position_within_image_bounds(mouse_relative_to_image_x, mouse_relative_to_image_y, captured_image):
                return
            callback(pixel, (cursor_image_pixel_x, cursor_image_pixel_y), (mouse_relative_to_image_x, mouse_relative_to_image_y))


def _paste_cursor_on_image(cursor_position: Tuple[int, int],
                           cursor_image: Image,
                           captured_image: Image,
                           window_info: WindowInfo):

    cursor_image_pixel_data = cursor_image.load()

    def paste_white_pixel(pixel: Tuple[int, int, int], source_pixel_position: Tuple[int, int], destination_pixel_position: Tuple[int, int]):
        if not _is_white_pixel(pixel):
            return
        captured_image.putpixel(destination_pixel_position, (_COLOUR_WHITE,) * _COLOURS_PER_PIXEL)

    def add_black_border_around_pixel(pixel: Tuple[int, int, int], source_pixel_position: Tuple[int, int], destination_pixel_position: Tuple[int, int]):
        _add_border_pixels(source_pixel_position, destination_pixel_position, cursor_image_pixel_data, captured_image,
                           cursor_image)

    _iterate_through_cursor_pixels(cursor_position, cursor_image, cursor_image_pixel_data, captured_image, window_info, paste_white_pixel)
    _iterate_through_cursor_pixels(cursor_position, cursor_image, cursor_image_pixel_data, captured_image, window_info, add_black_border_around_pixel)


def add_cursor_to_image(captured_image: Image, window_info: WindowInfo):
    flags, hcursor, cursor_position = win32gui.GetCursorInfo()

    if flags == _MOUSE_HIDDEN_FLAG:
        return

    cursor_image = capture.get_cursor_image(hcursor)

    if not bounds.is_mouse_over_target_application(cursor_position, cursor_image.size, window_info):
        return

    _paste_cursor_on_image(cursor_position, cursor_image, captured_image, window_info)
