from typing import Tuple

from PIL import Image

from magnifier.win32 import WindowInfo


def _is_position_within_rect(position: Tuple[int, int], rect: Tuple[int, int, int, int]):
    return rect[0] < position[0] < rect[0] + rect[2] and rect[1] < position[1] < rect[1] + rect[3]


def is_mouse_over_target_application(cursor_position: Tuple[int, int], window_info: WindowInfo) -> bool:
    size = window_info.size
    position = window_info.position
    return _is_position_within_rect(cursor_position, (position[0], position[1], size[0], size[1]))


def is_position_within_image_bounds(x: int, y: int, image: Image) -> bool:
    return _is_position_within_rect((x, y), (0, 0, image.size[0], image.size[1]))
