import tkinter as tk
from tkinter import ttk

from win32gui import EnumWindows, GetWindowText

from magnifier.util import Arguments
from .start_magnifier import start_magnifier


def _create_select_delay_section(root):
    text = tk.StringVar()
    text.set('Select capture interval delay (milliseconds) (50):')

    select_delay_duration_label = ttk.Label(root, textvariable=text)
    select_delay_duration_label.pack(fill='x', padx=5, pady=5)

    def on_magnification_changed(new_value):
        text.set(f'Select capture interval delay (milliseconds) ({round(float(new_value), 1)}):')

    delay_level_slider = ttk.Scale(root, from_=1, to=1000, orient=tk.HORIZONTAL, command=on_magnification_changed)
    delay_level_slider.set(50)
    delay_level_slider.pack(fill='x', padx=5, pady=5)

    return delay_level_slider


def _create_select_resampling_filter(root):
    select_resampling_filter_label = ttk.Label(root, text='Select a resampling filter (default is BICUBIC):')
    select_resampling_filter_label.pack(fill='x', padx=5, pady=5)

    resampling_filter_selector = ttk.Combobox(root)
    resampling_filter_selector['values'] = ['NEAREST (Quickest Lowest Quality)', 'BOX', 'BILINEAR', 'HAMMING', 'BICUBIC (Slower, Higher Quality)', 'LANCZOS (Slowest, Highest Quality)']
    resampling_filter_selector.pack(fill='x', padx=5, pady=5)

    return resampling_filter_selector


def _create_select_window_title_section(root):
    window_titles = []

    def add_title(hwnd, extra):
        window_titles.append(GetWindowText(hwnd))

    EnumWindows(add_title, None)

    window_titles = [title for title in window_titles if title is not None and title.strip() != '']
    window_titles.sort()

    select_window_label = ttk.Label(root, text='Select a target application to magnify:')
    select_window_label.pack(fill='x', padx=5, pady=5)

    window_title_selector = ttk.Combobox(root)
    window_title_selector['values'] = [title for title in window_titles if title is not None and title.strip() != '']
    window_title_selector.pack(fill='x', padx=5, pady=5)

    return window_title_selector


def _create_capture_cursor_checkbox(root):
    control = tk.StringVar(value=0)
    check = ttk.Checkbutton(root, text='Capture mouse cursor when cursor is over target window', variable=control)
    check.pack(fill='x', padx=5, pady=5)
    return control


def _create_always_on_top(root):
    control = tk.StringVar(value=1)
    check = ttk.Checkbutton(root, text='Make magnifier appear on top of other windows', variable=control)
    check.pack(fill='x', padx=5, pady=5)
    return control


def _create_refocus_to_target(root):
    control = tk.StringVar(value=1)
    check = ttk.Checkbutton(root, text='Activate target window when magnifier is selected', variable=control)
    check.pack(fill='x', padx=5, pady=5)
    return control


def _parse_resampling_filter_option(sampler_option: str) -> str:
    sampler_option = sampler_option.strip()
    if sampler_option == '':
        return 'BICUBIC'

    if ' ' in sampler_option:
        return sampler_option.split(' ')[0].strip()

    return sampler_option


def present_magnifier_options():
    root = tk.Tk()
    root.geometry('450x315')
    root.resizable(False, False)
    root.title('Window Magnifier Options')

    window_title_selector = _create_select_window_title_section(root)
    delay_level_slider = _create_select_delay_section(root)
    sample_selector = _create_select_resampling_filter(root)
    capture_cursor_check = _create_capture_cursor_checkbox(root)
    always_on_top_check = _create_always_on_top(root)
    refocus_to_target_check = _create_refocus_to_target(root)

    def confirm_clicked():
        window_title = window_title_selector.get()
        capture_delay_interval = round(float(delay_level_slider.get()) / 1000.0, 5)
        resampling_filter = _parse_resampling_filter_option(sample_selector.get())
        capture_cursor = capture_cursor_check.get() == '1'
        always_on_top = always_on_top_check.get() == '1'
        refocus_to_target = refocus_to_target_check.get() == '1'
        if window_title.strip() == '':
            return
        arguments = Arguments(window_title, capture_delay_interval, resampling_filter, capture_cursor, always_on_top,
                              refocus_to_target)
        print(str(arguments))
        root.destroy()
        start_magnifier(arguments)

    confirm_button = ttk.Button(root, text="Magnify", command=confirm_clicked)
    confirm_button.pack(fill='x', padx=5, pady=5)

    root.mainloop()


if __name__ == '__main__':
    present_magnifier_options()
