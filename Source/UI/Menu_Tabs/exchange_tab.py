import tkinter as tk
from Source.Config import style


def build_exchange_tab(parent, settings, config):

    tk.Label(
        parent,
        text="Exchange",
        font=style.TITLE_FONT
    ).pack(pady=10)

    tk.Label(
        parent,
        text="Comming soon",
        font= style.TEXT_FONT

    ).pack(
        pady=20
    )