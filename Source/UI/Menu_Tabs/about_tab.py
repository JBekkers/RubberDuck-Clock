import tkinter as tk

from Source.Config import style
from Source.UI.Menu_Tabs.stats import get_session_uptime
from Source.animation import animations


def format_uptime(seconds):
    hours = seconds / 3600
    return f"Total Uptime:\n{hours:.1f} hours"


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
        text="Duck Clock is a simple, lightweight clock with a cute duck-themed design. It started as a small Python project but quickly became a passion project combining my love of coding and collecting ducks.",
        font=style.TEXT_FONT,
        wraplength=300
    ).pack(
        pady=(0, 10)
    )

    tk.Label(
        parent,
        text="App Stats",
        font=style.TITLE_FONT
    ).pack(
        pady=(10, 5)
    )

    uptime_display = tk.StringVar()
    session_display = tk.StringVar()
    rare_display = tk.StringVar()

    uptime_label = tk.Label(
        parent,
        textvariable=uptime_display,
        font=style.TEXT_FONT
    )

    uptime_label.pack()

    session_label = tk.Label(
        parent,
        textvariable=session_display,
        font=style.TEXT_FONT
    )

    session_label.pack(
        pady=(15, 0)
    )

    rare_label = tk.Label(
        parent,
        textvariable=rare_display,
        font=style.TEXT_FONT
    )

    rare_label.pack(
        pady=(15, 0)
    )

    def update_uptime():

        current_session = get_session_uptime()

        total_uptime = (
            config.get("total_uptime", 0)
            + current_session
        )

        uptime_display.set(
            format_uptime(total_uptime)
        )

        session_display.set(
            f"Total Sessions:\n"
            f"{config.get('session_count', 0)}"
        )

        discovered = len(
            config.get(
                "rare_animations_discovered",
                []
            )
        )

        rare_count = sum(
            1 for animation in animations.values()
            if animation.isRare
        )

        rare_display.set(
            f"Rare Animations:\n"
            f"{config.get('rare_animations_seen', 0)} seen  •  "
            f"{discovered} / {rare_count} discovered"
        )

        uptime_label.after(
            1000,
            update_uptime
        )

    update_uptime()

    tk.Label(
        parent,
        text="Version: DEV_1.0.0\n\n"
        "Created by Epicstargamer (Esg)\n"
        "Made using Python and TKinter",
        font=style.TEXT_FONT
    ).pack(
        pady=20
    )