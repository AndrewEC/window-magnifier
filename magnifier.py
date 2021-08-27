import tkinter as tk
from tkinter import ttk

import pygetwindow as gw

from arguments import Arguments
from start_magnifier import start_magnifier


def create_select_magnification_section(root):
    text = tk.StringVar()
    text.set('Enter magnification level (2.2):')

    select_magnification_level_label = ttk.Label(root, textvariable=text)
    select_magnification_level_label.pack(fill='x', padx=5, pady=5)

    def on_magnification_changed(new_value):
        text.set(f'Enter magnification level ({round(float(new_value), 1)}):')

    magnification_level_slider = ttk.Scale(root, from_=0.1, to=20, orient=tk.HORIZONTAL, command=on_magnification_changed)
    magnification_level_slider.set(2.2)
    magnification_level_slider.pack(fill='x', padx=5, pady=5)

    return magnification_level_slider


def create_select_window_title_section(root):
    select_window_label = ttk.Label(root, text='Select a window to Magnify:')
    select_window_label.pack(fill='x', padx=5, pady=5)

    window_titles = [title for title in gw.getAllTitles() if title.strip() != '']
    window_title_selector = ttk.Combobox(root)
    window_title_selector['values'] = window_titles
    window_title_selector.pack(fill='x', padx=5, pady=5)

    return window_title_selector


def present_ui():
    root = tk.Tk()
    root.geometry('450x180')
    root.resizable(False, False)
    root.title('Window Magnifier Options')

    window_title_selector = create_select_window_title_section(root)
    magnification_level_slider = create_select_magnification_section(root)

    def confirm_clicked():
        window_title = window_title_selector.get()
        magnification_level = round(float(magnification_level_slider.get()), 1)
        if window_title.strip() == '':
            return
        arguments = Arguments(window_title, magnification_level)
        root.destroy()
        start_magnifier(arguments)

    confirm_button = ttk.Button(root, text="Magnify", command=confirm_clicked)
    confirm_button.pack(fill='x', padx=5, pady=5)

    root.mainloop()


if __name__ == '__main__':
    present_ui()
