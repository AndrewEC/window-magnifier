from typing import Tuple


def upscale_size_by(size: Tuple[int, int], scale_factor: float) -> Tuple[int, int]:
    return int(size[0] * scale_factor), int(size[1] * scale_factor)


def calculate_new_scale_factor(source_size: Tuple[int, int], destination_size: Tuple[int, int]) -> float:
    scale = destination_size[0] / source_size[0]
    if source_size[1] * scale > destination_size[1]:
        scale = destination_size[1] / source_size[1]
    return scale
