import tkinter as tk
from Source.Config import style


def build_about_tab(parent, settings, config):

    tk.Label(
        parent,
        text="About",
        font=style.TITLE_FONT,
    ).pack(pady=20)

    tk.Label(
        parent,
        text="Version 1.0.0",
        font= style.TEXT_FONT
    ).pack()

    tk.Label(
        parent,
        text="Created by Epicstargamer (Esg)",
        font= style.TEXT_FONT
    ).pack(
        pady=20
    )