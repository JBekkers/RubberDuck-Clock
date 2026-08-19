import tkinter as tk
import time

from Source.Config import style
from Source.UI.Menu_Tabs.uptime import get_session_uptime


def format_uptime(seconds):

    seconds = int(seconds)

    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"

    return f"{minutes}m"


def build_about_tab(parent, settings, config):

    tk.Label(
        parent,
        text="About",
        font=style.TITLE_FONT,
    ).pack(
        pady=20
    )

    tk.Label(
        parent,
        text="Version 1.0.0",
        font=style.TEXT_FONT
    ).pack()

    tk.Label(
        parent,
        text="Created by Epicstargamer (Esg)",
        font=style.TEXT_FONT
    ).pack(
        pady=20
    )

    tk.Label(
        parent,
        text="Total Uptime",
        font=style.TITLE_FONT
    ).pack(
        pady=(10, 5)
    )

    uptime_display = tk.StringVar()

    uptime_label = tk.Label(
        parent,
        textvariable=uptime_display,
        font=style.TEXT_FONT
    )

    uptime_label.pack()

    def update_uptime():

        current_session = get_session_uptime()

        total_uptime = (
            config.get("total_uptime", 0)
            +
            current_session
        )

        uptime_display.set(
            format_uptime(total_uptime)
        )

        uptime_label.after(
            1000,
            update_uptime
        )

    update_uptime()