import tkinter as tk
from tkinter import ttk

from Source.UI.Menu_Tabs.cosmetics_tab import build_cosmetics_tab
from Source.UI.Menu_Tabs.settings_tab import build_settings_tab
from Source.UI.Menu_Tabs.about_tab import build_about_tab
from Source.UI.Menu_Tabs.exchange_tab import build_exchange_tab

window = None


def open_settings(root, settings, config, actions):

    global window

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

        if builder is build_settings_tab:
            builder(frame, settings, config, actions)
        else:
            builder(frame, settings, config)

