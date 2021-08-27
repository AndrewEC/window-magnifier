import tkinter as tk
from tkinter import ttk

from win32gui import EnumWindows, GetWindowText

from magnifier.util import Arguments
from .start_magnifier import start_magnifier


def create_select_delay_section(root):
    text = tk.StringVar()
    text.set('Select capture interval delay (milliseconds) (10):')

    select_delay_duration_label = ttk.Label(root, textvariable=text)
    select_delay_duration_label.pack(fill='x', padx=5, pady=5)

    def on_magnification_changed(new_value):
        text.set(f'Select capture interval delay (milliseconds) ({round(float(new_value), 1)}):')

    delay_level_slider = ttk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, command=on_magnification_changed)
    delay_level_slider.set(10)
    delay_level_slider.pack(fill='x', padx=5, pady=5)

    return delay_level_slider


def create_select_resampling_filter(root):
    select_resampling_filter_label = ttk.Label(root, text='Select a resampling filter (default is BICUBIC):')
    select_resampling_filter_label.pack(fill='x', padx=5, pady=5)

    resampling_filter_selector = ttk.Combobox(root)
    resampling_filter_selector['values'] = ['NEAREST (Quickest Lowest Quality)', 'BOX', 'BILINEAR', 'HAMMING', 'BICUBIC (Slower, Higher Quality)', 'LANCZOS (Slowest, Highest Quality)']
    resampling_filter_selector.pack(fill='x', padx=5, pady=5)

    return resampling_filter_selector


def create_select_window_title_section(root):
    window_titles = []

    def add_title(hwnd, extra):
        window_titles.append(GetWindowText(hwnd))

    EnumWindows(add_title, None)

    window_titles = [title for title in window_titles if title is not None and title.strip() != '']
    window_titles.sort()

    select_window_label = ttk.Label(root, text='Select a window to Magnify:')
    select_window_label.pack(fill='x', padx=5, pady=5)

    window_title_selector = ttk.Combobox(root)
    window_title_selector['values'] = [title for title in window_titles if title is not None and title.strip() != '']
    window_title_selector.pack(fill='x', padx=5, pady=5)

    return window_title_selector


def create_capture_cursor_checkbox(root):
    def do():
        pass

    control = tk.StringVar(value=0)
    check = ttk.Checkbutton(root, text='Capture mouse cursor', command=do, variable=control)
    check.pack(fill='x', padx=5, pady=5)
    return control


def parse_resampling_filter_option(raw_option: str) -> str:
    raw_option = raw_option.strip()
    if raw_option == '':
        return 'BICUBIC'

    if ' ' in raw_option:
        return raw_option.split(' ')[0].strip()

    return raw_option


def present_ui():
    root = tk.Tk()
    root.geometry('450x260')
    root.resizable(False, False)
    root.title('Window Magnifier Options')

    window_title_selector = create_select_window_title_section(root)
    delay_level_slider = create_select_delay_section(root)
    sample_selector = create_select_resampling_filter(root)
    capture_cursor_check = create_capture_cursor_checkbox(root)

    def confirm_clicked():
        window_title = window_title_selector.get()
        capture_delay_interval = round(float(delay_level_slider.get()) / 1000.0, 5)
        resampling_filter = parse_resampling_filter_option(sample_selector.get())
        capture_cursor = capture_cursor_check.get() == '1'
        if window_title.strip() == '':
            return
        arguments = Arguments(window_title, capture_delay_interval, resampling_filter, capture_cursor)
        print(str(arguments))
        root.destroy()
        start_magnifier(arguments)

    confirm_button = ttk.Button(root, text="Magnify", command=confirm_clicked)
    confirm_button.pack(fill='x', padx=5, pady=5)

    root.mainloop()


if __name__ == '__main__':
    present_ui()
