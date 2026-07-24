import tkinter as tk
from tkinter import ttk

from Source.UI.Menu_Tabs.cosmetics_tab import build_cosmetics_tab
from Source.UI.Menu_Tabs.settings_tab import build_settings_tab
from Source.UI.Menu_Tabs.about_tab import build_about_tab
from Source.UI.Menu_Tabs.exchange_tab import build_exchange_tab

window = None
window_width = 400

BACKGROUND = "#FDFF85"
BUTTON = "#FFBA53"
TEXT = "#000000"


def open_settings(root, settings, config, actions):

    global window

    if window is not None and window.winfo_exists():
        window.focus_force()
        return

    window = tk.Toplevel(root)

    window.title("Duck Clock")
    window.geometry(f"{window_width}x450")
    window.resizable(False, False)

    tab_bar = tk.Frame(
    window,
    bg= BACKGROUND
    )
    tab_bar.pack(fill="x")

    content = tk.Frame(
    window,
    bg= BACKGROUND
    )

    content.pack(
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

    frames = []

    def show_tab(index):
        for frame in frames:
            frame.pack_forget()

        frames[index].pack(
            fill="both",
            expand=True
        )

    for index, (title, builder) in enumerate(tabs):

        tab_bar.columnconfigure(index, weight=1)

        button = tk.Button(
            tab_bar,
            text  =title,
            command=lambda i=index: show_tab(i),
            bg=BACKGROUND,
            fg=TEXT,
            relief="flat",
            borderwidth=0
        )

        button.grid(
            row=0,
            column=index,
            sticky="ew"
        )

        frame = ttk.Frame(content)
        frames.append(frame)

        if builder is build_settings_tab:
            builder(frame, settings, config, actions)
        else:
            builder(frame, settings, config)

    show_tab(0)