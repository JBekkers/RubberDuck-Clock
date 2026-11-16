
import tkinter as tk

from Source.Config import style


def build_planning_tab(parent, settings, config, hat_manager):
    tk.Label(
        parent,
        text="Coming Soon!",
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(
        expand=True
    )
