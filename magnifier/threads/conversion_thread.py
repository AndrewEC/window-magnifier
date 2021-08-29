import time
from queue import Queue

from PIL import Image
import pygame

from magnifier.util import ScaleContainer, upscale_size_by, Arguments

from .window_locator import WindowInfoContainer
from .countdown_latch import CountDownLatch
from .base_thread import BaseThread


class ConversionThread(BaseThread):

    def __init__(self, capture_queue: Queue, conversion_queue: Queue, window_info_container: WindowInfoContainer,
                 scale_container: ScaleContainer, latch: CountDownLatch, arguments: Arguments):
        super().__init__('ConversionThread', latch)
        self._capture_queue = capture_queue
        self._window_info_container = window_info_container
        self._scale_container = scale_container
        self._conversion_queue = conversion_queue
        self._arguments = arguments

    def execute(self):
        try:
            capture_data = self._capture_queue.get(True, 0.1)
            image = self._upscale_image(capture_data)
            surface = self._convert_image_to_surface(image)
            self._conversion_queue.put(surface)
        except Exception:
            time.sleep(0.01)

    def _upscale_image(self, captured_image: Image) -> Image:
        current_size = self._window_info_container.get_window_info().size
        target_size = self._scale_container.get_scale()
        resampling_filter = getattr(Image, self._arguments.resampling_filter)
        return captured_image.resize(upscale_size_by(current_size, target_size), resampling_filter)

    def _convert_image_to_surface(self, pil: Image):
        return pygame.image.fromstring(pil.tobytes(), pil.size, pil.mode).convert()


def start_conversion_thread(capture_queue: Queue, conversion_queue: Queue, window_info_container: WindowInfoContainer,
                            scale_container: ScaleContainer, latch: CountDownLatch, arguments: Arguments)\
        -> ConversionThread:
    conversion_thread = ConversionThread(capture_queue, conversion_queue, window_info_container, scale_container,
                                         latch, arguments)
    conversion_thread.start()
    return conversion_thread
