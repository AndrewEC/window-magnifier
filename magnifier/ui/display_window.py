from typing import Callable
from queue import Queue

import win32con
import win32gui
import pygame
from pygame.event import Event

from magnifier.util import ScaleContainer, calculate_new_scale_factor, MAGNIFIER_DISPLAY_WINDOW_NAME, Arguments,\
    invoke_and_suppress, WindowHandleContainer, get_icon_path
from magnifier.win32 import get_window_info, get_window_handle


def _determine_image_rect(image_rect: pygame.Rect):
    width, height = pygame.display.get_surface().get_size()
    return pygame.Rect(width / 2 - image_rect.width / 2, height / 2 - image_rect.height / 2, image_rect.width, image_rect.height)


def _set_window_to_be_on_top():
    hwnd = pygame.display.get_wm_info()['window']
    position = get_window_info(hwnd).position
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, position[0], position[1], 0, 0,
                          win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def _update_scale_factor(event: Event, window_handle, scale_container: ScaleContainer):
    window_info = get_window_info(window_handle)
    size = event.dict['size']
    new_scale = calculate_new_scale_factor(window_info.size, size)
    scale_container.set_value(new_scale)


def start_display_window(conversion_queue: Queue, window_handle_container: WindowHandleContainer,
                         scale_container: ScaleContainer, arguments: Arguments, on_exit: Callable):
    window_handle = window_handle_container.get_value()

    icon_path = get_icon_path()
    if icon_path is not None:
        pygame.display.set_icon(pygame.image.load(icon_path))
    pygame.init()

    size = get_window_info(window_handle).size
    print(f'Initializing pygame window to [{size}]')

    pygame_screen = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption(MAGNIFIER_DISPLAY_WINDOW_NAME)

    if arguments.always_on_top:
        invoke_and_suppress(_set_window_to_be_on_top)

    while True:
        if not win32gui.IsWindow(window_handle):
            window_handle = get_window_handle(arguments.target_window_title)
            if window_handle is None:
                pygame.time.delay(500)
            else:
                window_handle_container.set_value(window_handle)
                invoke_and_suppress(lambda: _update_scale_factor(event, window_handle, scale_container))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return on_exit()
            elif event.type == pygame.VIDEORESIZE:
                invoke_and_suppress(lambda: _update_scale_factor(event, window_handle, scale_container))
            elif event.type == pygame.WINDOWFOCUSGAINED:
                if arguments.refocus_to_target:
                    invoke_and_suppress(lambda: win32gui.SetForegroundWindow(window_handle))

        try:
            next_image = conversion_queue.get(True, timeout=0.3)

            pygame_screen.fill((0, 0, 0))
            pygame_screen.blit(next_image, _determine_image_rect(next_image.get_rect()))
        except:
            pass

        pygame.display.flip()
        pygame.display.update()
