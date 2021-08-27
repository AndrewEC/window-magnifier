from typing import Tuple


def upscale_size_by(size: Tuple[int, int], scale_up_by: float) -> Tuple[int, int]:
    return int(size[0] * scale_up_by), int(size[1] * scale_up_by)


def calculate_new_scale(source_size: Tuple[int, int], destination_size: Tuple[int, int]) -> float:
    scale = destination_size[0] / source_size[0]
    if source_size[1] * scale > destination_size[1]:
        scale = destination_size[1] / source_size[1]
    return scale
