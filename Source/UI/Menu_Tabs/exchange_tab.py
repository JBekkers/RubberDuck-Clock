import tkinter as tk
from Source.Config import style


def build_exchange_tab(parent, settings, config):

    tk.Label(
        parent,
        text="Exchange",
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(
        pady=(10)
    )

    tk.Label(
        parent,
        text="Exchange features are coming soon.",
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.MUTED_TEXT,
        wraplength=300,
        justify="center"
    ).pack(
        pady=20,
        padx=20
    )