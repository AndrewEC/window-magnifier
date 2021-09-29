import time
from queue import Queue

from PIL import Image
import pygame
from pygame import Surface

from magnifier.util import ScaleContainer, upscale_size_by, Arguments, WindowHandleContainer
from magnifier.win32 import get_window_info

from .countdown_latch import CountDownLatch
from .base_thread import BaseThread


class ResizeThread(BaseThread):

    def __init__(self, capture_queue: Queue, conversion_queue: Queue, window_handle_container: WindowHandleContainer,
                 scale_container: ScaleContainer, latch: CountDownLatch, arguments: Arguments):
        super().__init__('ConversionThread', latch)
        self._capture_queue = capture_queue
        self._scale_container = scale_container
        self._conversion_queue = conversion_queue
        self._arguments = arguments
        self._window_handle = window_handle_container.get_value()
        self._window_handle_container = window_handle_container

    def execute(self):
        try:
            capture_data = self._capture_queue.get(True, 0.3)
            image = self._upscale_image(capture_data)
            surface = self._convert_image_to_surface(image)
            self._conversion_queue.put(surface)
        except Exception:
            time.sleep(0.5)
            self._window_handle = self._window_handle_container.get_value()

    def _upscale_image(self, captured_image: Image) -> Image:
        current_size = get_window_info(self._window_handle).size
        scale_factor = self._scale_container.get_value()
        resampling_filter = getattr(Image, self._arguments.resampling_filter)
        return captured_image.resize(upscale_size_by(current_size, scale_factor), resampling_filter)

    def _convert_image_to_surface(self, pil: Image) -> Surface:
        return pygame.image.fromstring(pil.tobytes(), pil.size, pil.mode).convert()


def start_resize_thread(capture_queue: Queue, conversion_queue: Queue, window_handle_container: WindowHandleContainer,
                        scale_container: ScaleContainer, latch: CountDownLatch, arguments: Arguments)\
        -> ResizeThread:
    conversion_thread = ResizeThread(capture_queue, conversion_queue, window_handle_container, scale_container,
                                     latch, arguments)
    conversion_thread.start()
    return conversion_thread
