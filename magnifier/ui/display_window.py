from typing import Callable

from queue import Queue

import pygame

from magnifier.threads import WindowInfoContainer
from magnifier.util import ScaleContainer, calculate_new_scale


def determine_image_rect(image_rect: pygame.Rect):
    width, height = pygame.display.get_surface().get_size()
    return pygame.Rect(width / 2 - image_rect.width / 2, height / 2 - image_rect.height / 2, image_rect.width, image_rect.height)


def start_display_window(conversion_queue: Queue, window_info: WindowInfoContainer, scale_container: ScaleContainer,
                         on_exit: Callable):
    pygame.init()

    size = window_info.get_window_info().size
    print(f'Initializing pygame window to [{size}]')

    pygame_screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return on_exit()
            elif event.type == pygame.VIDEORESIZE:
                size = event.dict['size']
                new_scale = calculate_new_scale(window_info.get_window_info().size, size)
                scale_container.set_scale(new_scale)

        try:
            next_image = conversion_queue.get(True, timeout=0.3)

            pygame_screen.fill((0, 0, 0))
            pygame_screen.blit(next_image, determine_image_rect(next_image.get_rect()))
        except Exception:
            pass

        pygame.display.flip()
        pygame.display.update()
