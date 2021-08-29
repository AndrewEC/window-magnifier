from typing import Callable
from queue import Queue

import win32con
import win32gui
import pygame

from magnifier.threads import WindowInfoContainer
from magnifier.util import ScaleContainer, calculate_new_scale, MAGNIFIER_DISPLAY_WINDOW_NAME, Arguments
from magnifier.win32 import get_core_window_info_by_hwnd


def determine_image_rect(image_rect: pygame.Rect):
    width, height = pygame.display.get_surface().get_size()
    return pygame.Rect(width / 2 - image_rect.width / 2, height / 2 - image_rect.height / 2, image_rect.width, image_rect.height)


def start_display_window(conversion_queue: Queue, window_info_container: WindowInfoContainer, scale_container: ScaleContainer,
                         arguments: Arguments, on_exit: Callable):
    pygame.init()

    size = window_info_container.get_window_info().size
    print(f'Initializing pygame window to [{size}]')

    pygame_screen = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption(MAGNIFIER_DISPLAY_WINDOW_NAME)

    if arguments.always_on_top:
        hwnd = pygame.display.get_wm_info()['window']
        position = get_core_window_info_by_hwnd(hwnd).position
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, position[0], position[1], 0, 0,
                              win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return on_exit()
            elif event.type == pygame.VIDEORESIZE:
                window_info = window_info_container.get_window_info()
                if not window_info.is_default_info():
                    size = event.dict['size']
                    new_scale = calculate_new_scale(window_info_container.get_window_info().size, size)
                    scale_container.set_scale(new_scale)
            elif event.type == pygame.WINDOWFOCUSGAINED:
                try:
                    if arguments.refocus_to_target:
                        win32gui.SetForegroundWindow(window_info_container.get_window_info().window_handle)
                except Exception:
                    pass

        try:
            next_image = conversion_queue.get(True, timeout=0.3)

            pygame_screen.fill((0, 0, 0))
            pygame_screen.blit(next_image, determine_image_rect(next_image.get_rect()))
        except Exception:
            pass

        pygame.display.flip()
        pygame.display.update()
