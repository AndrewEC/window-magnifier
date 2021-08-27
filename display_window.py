from typing import Callable

from queue import Queue

import pygame

from window_locator import WindowInfoContainer
from arguments import Arguments


def start_display_window(conversion_queue: Queue, window_info: WindowInfoContainer, arguments: Arguments, on_exit: Callable):
    pygame.init()

    size = window_info.get_window_info().get_scaled_size(arguments.upscale_modifier)
    print(f'Initializing pygame window to [{size}]')

    pygame_screen = pygame.display.set_mode(size)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on_exit()

        try:
            next_image = conversion_queue.get(True, timeout=0.3)

            pygame_screen.fill((0, 0, 0))
            pygame_screen.blit(next_image, next_image.get_rect())
        except Exception:
            pass

        pygame.display.flip()
        pygame.display.update()
