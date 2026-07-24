import tkinter as tk
from tkinter import ttk

from Source.Settings_Menu.Cosmetics_Tab import build_cosmetics_tab
from Source.Settings_Menu.Settings_Tab import build_settings_tab
from Source.Settings_Menu.About_Tab import build_about_tab
from Source.Settings_Menu.Exchange_Tab import build_exchange_tab

window = None


def open_settings(root, settings, config):

    global window

    # Don't allow multiple windows
    if window is not None and window.winfo_exists():
        window.focus_force()
        return

    window = tk.Toplevel(root)

    window.title("Duck Clock")

    window.geometry("400x450")

    window.resizable(False, False)

    notebook = ttk.Notebook(window)

    notebook.pack(
        fill="both",
        expand=True,
        padx=5,
        pady=5
    )

    tabs = [
    ("Cosmetics", build_cosmetics_tab),
    ("Exchange", build_exchange_tab),
    ("Settings", build_settings_tab),
    ("About", build_about_tab),
]

    for title, builder in tabs:
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        builder(frame, settings, config)

