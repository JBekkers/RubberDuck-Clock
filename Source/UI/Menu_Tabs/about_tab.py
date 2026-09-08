import tkinter as tk
from tkinter import ttk

from Source.Config import style
from Source.UI.Menu_Tabs.stats import get_session_uptime
from Source.animation import animations


def format_uptime(seconds):
    hours = seconds / 3600
    return f"Total Uptime:\n{hours:.1f} hours"


def build_about_tab(parent, settings, config, stats):

    scroll_container = tk.Frame(parent)
    scroll_container.pack(
        fill="both",
        expand=True
    )

    scrollbar_style = ttk.Style()
    scrollbar_style.theme_use("clam")

    scrollbar_style.configure(
        "About.Vertical.TScrollbar",
        background=style.SCROLL_BACKGROUND,
        troughcolor=style.SCROLL_TROUGH,
        bordercolor=style.SCROLL_BORDER,
        arrowcolor=style.SCROLL_ARROW,
        relief="flat",
        width=14
    )

    scrollbar_style.map(
        "About.Vertical.TScrollbar",
        background=[
            ("active", style.BUTTON_CLICKED),
            ("pressed", style.BUTTON_CLICKED)
        ]
    )

    scrollbar = ttk.Scrollbar(
        scroll_container,
        orient="vertical",
        style="About.Vertical.TScrollbar"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    scroll_canvas = tk.Canvas(
        scroll_container,
        highlightthickness=0,
        yscrollcommand=scrollbar.set
    )

    scroll_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=scroll_canvas.yview
    )

    about_frame = tk.Frame(
        scroll_canvas
    )

    about_window = scroll_canvas.create_window(
        (0, 0),
        window=about_frame,
        anchor="nw"
    )

    def update_scroll_region(event=None):
        scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")
        )

    about_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    def resize_about_frame(event):
        scroll_canvas.itemconfig(
            about_window,
            width=event.width
        )

    scroll_canvas.bind(
        "<Configure>",
        resize_about_frame
    )

    def mouse_wheel(event):
        scroll_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def enable_mousewheel(event):
        scroll_canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel
        )

    def disable_mousewheel(event):
        scroll_canvas.unbind_all(
            "<MouseWheel>"
        )

    scroll_canvas.bind(
        "<Enter>",
        enable_mousewheel
    )

    scroll_canvas.bind(
        "<Leave>",
        disable_mousewheel
    )

    tk.Label(
        about_frame,
        text="About",
        font=style.TITLE_FONT
    ).pack(
        pady=20
    )

    tk.Label(
        about_frame,
        text=(
            "Duck Clock is a simple, lightweight clock with a cute "
            "duck-themed design. It started as a small Python project "
            "but quickly became a passion project combining my love "
            "of coding and collecting ducks."
        ),
        font=style.TEXT_FONT,
        wraplength=300
    ).pack(
        pady=(0, 10)
    )

    tk.Label(
        about_frame,
        text="App Stats",
        font=style.TITLE_FONT
    ).pack(
        pady=(10, 5)
    )

    uptime_display = tk.StringVar()
    session_display = tk.StringVar()
    rare_display = tk.StringVar()

    tk.Label(
        about_frame,
        textvariable=uptime_display,
        font=style.TEXT_FONT
    ).pack()

    tk.Label(
        about_frame,
        textvariable=session_display,
        font=style.TEXT_FONT
    ).pack(
        pady=(15, 0)
    )

    rare_title_frame = tk.Frame(
        about_frame,
        bg=style.BACKGROUND
    )

    rare_title_frame.pack(
        pady=(15, 0)
    )

    tk.Label(
        rare_title_frame,
        text="Rare Animations:",
        font=style.TEXT_FONT,
        bg=style.BACKGROUND
    ).pack(
        side="left"
    )

    rare_info = tk.Label(
        rare_title_frame,
        text="ⓘ",
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR,
        cursor="hand2"
    )

    rare_info.pack(
        side="left",
        padx=(5, 0)
    )

    rare_label = tk.Label(
        about_frame,
        textvariable=rare_display,
        font=style.TEXT_FONT
    )

    rare_label.pack()

    rare_details_container = tk.Frame(
        about_frame,
        bg=style.BACKGROUND
    )

    rare_scrollbar = ttk.Scrollbar(
        rare_details_container,
        orient="vertical"
    )

    rare_scrollbar.pack(
        side="right",
        fill="y"
    )

    rare_canvas = tk.Canvas(
        rare_details_container,
        height=100,
        highlightthickness=0,
        bg=style.BACKGROUND,
        yscrollcommand=rare_scrollbar.set
    )

    rare_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    rare_scrollbar.config(
        command=rare_canvas.yview
    )

    rare_list_frame = tk.Frame(
        rare_canvas,
        bg=style.BACKGROUND
    )

    rare_list_window = rare_canvas.create_window(
        (0, 0),
        window=rare_list_frame,
        anchor="nw"
    )

    def update_rare_scroll_region(event=None):
        rare_canvas.configure(
            scrollregion=rare_canvas.bbox("all")
        )

    rare_list_frame.bind(
        "<Configure>",
        update_rare_scroll_region
    )

    def resize_rare_list(event):
        rare_canvas.itemconfig(
            rare_list_window,
            width=event.width
        )

    rare_canvas.bind(
        "<Configure>",
        resize_rare_list
    )

    def update_rare_details():
        for widget in rare_list_frame.winfo_children():
            widget.destroy()

        counts = stats.get(
            "rare_animation_counts",
            {}
        )

        rare_animations = [
            name
            for name, animation in animations.items()
            if animation.isRare
        ]

        for name in rare_animations:
            count = counts.get(
                name,
                0
            )

            tk.Label(
                rare_list_frame,
                text=f"{name}  ×{count}",
                font=style.TEXT_FONT,
                bg=style.BACKGROUND,
                fg=(
                    "#168a28"
                    if count > 0
                    else "#c62828"
                ),
                anchor="w"
            ).pack(
                fill="x",
                pady=1
            )

        rare_list_frame.update_idletasks()

        rare_canvas.configure(
            scrollregion=rare_canvas.bbox("all")
        )

    def toggle_rare_details():
        if rare_details_container.winfo_manager():
            rare_details_container.pack_forget()
            return

        update_rare_details()

        rare_details_container.pack(
            fill="x",
            padx=20,
            pady=(5, 0)
        )

        scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")
        )

    rare_info.bind(
        "<Button-1>",
        lambda event: toggle_rare_details()
    )

    rare_info.bind(
        "<Enter>",
        lambda event: rare_info.config(
            fg=style.BUTTON_CLICKED
        )
    )

    rare_info.bind(
        "<Leave>",
        lambda event: rare_info.config(
            fg=style.TEXT_COLOR
        )
    )

    def update_uptime():
        current_session = get_session_uptime()

        total_uptime = (
            stats.get(
                "total_uptime",
                0
            )
            + current_session
        )

        uptime_display.set(
            format_uptime(total_uptime)
        )

        session_display.set(
            f"Total Sessions:\n"
            f"{stats.get('session_count', 0)}"
        )

        discovered = len(
            stats.get(
                "rare_animations_discovered",
                []
            )
        )

        rare_count = sum(
            1
            for animation in animations.values()
            if animation.isRare
        )

        rare_display.set(
            f"{stats.get('rare_animations_seen', 0)} seen  •  "
            f"{discovered} / {rare_count} discovered"
        )

        rare_label.after(
            1000,
            update_uptime
        )

    update_uptime()

    tk.Label(
        about_frame,
        text=(
            "Version: DEV_1.0.0\n\n"
            "Created by Epicstargamer (Esg)\n"
            "Made using Python and TKinter"
        ),
        font=style.TEXT_FONT
    ).pack(
        pady=20
    )