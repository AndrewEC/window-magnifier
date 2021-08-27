import time
from threading import Thread
from queue import Queue

from mss.screenshot import ScreenShot
from PIL import Image
import pygame

from arguments import Arguments
from window_locator import WindowInfoContainer


class ConversionThread(Thread):

    def __init__(self, capture_queue: Queue, conversion_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments):
        super().__init__()
        self._running = True
        self._capture_queue = capture_queue
        self._arguments = arguments
        self._window_info = window_info_container
        self._conversion_queue = conversion_queue

    def run(self):
        print('Starting conversion thread')
        while self._running:
            try:
                capture_data = self._capture_queue.get(True, 0.1)
                image = self._convert_to_pil_image(capture_data)
                surface = self._convert_image_to_surface(image)
                self._conversion_queue.put(surface)
            except Exception:
                time.sleep(0.01)
        print('Conversion thread stopped')

    def _convert_to_pil_image(self, capture_data: ScreenShot) -> Image:
        pil_image = Image.frombytes("RGB", capture_data.size, capture_data.bgra, "raw", "BGRX")
        return pil_image.resize(self._window_info.get_window_info().get_scaled_size(self._arguments.upscale_modifier))

    def _convert_image_to_surface(self, pil: Image):
        return pygame.image.fromstring(pil.tobytes(), pil.size, pil.mode).convert()

    def stop_running(self):
        print('Conversion thread stop requested.')
        self._running = False


def start_conversion_thread(capture_queue: Queue, conversion_queue: Queue, window_info_container: WindowInfoContainer, arguments: Arguments)\
        -> ConversionThread:
    conversion_thread = ConversionThread(capture_queue, conversion_queue, window_info_container, arguments)
    conversion_thread.start()
    return conversion_thread
