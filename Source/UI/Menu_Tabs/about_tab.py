import tkinter as tk
from tkinter import ttk

from Source.Config import style
from Source.UI.Menu_Tabs.stats import get_session_uptime
from Source.animation import animations


def format_uptime(seconds):
    hours = seconds / 3600
    return f"Total Uptime:\n{hours:.1f} hours"


def get_panel_color(color):
    color = color.lstrip("#")

    if len(color) != 6:
        return color

    rgb = [
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:6], 16)
    ]

    amount = -10 if sum(rgb) / 3 > 128 else 12

    rgb = [
        max(0, min(255, value + amount))
        for value in rgb
    ]

    return "#" + "".join(f"{value:02x}" for value in rgb)


def build_about_tab(parent, settings, config, stats):
    last_discovered_animations = None

    scroll_container = tk.Frame(parent)
    scroll_container.pack(fill="both", expand=True)

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

    scroll_canvas = tk.Canvas(
        scroll_container,
        highlightthickness=0,
        bg=style.BACKGROUND,
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
        scroll_canvas,
        bg=style.BACKGROUND
    )

    about_window = scroll_canvas.create_window(
        (0, 0),
        window=about_frame,
        anchor="nw"
    )

    rare_panel_bg = get_panel_color(style.BACKGROUND)
    rare_border = get_panel_color(rare_panel_bg)

    def update_scrollbar():
        scroll_canvas.update_idletasks()
        about_frame.update_idletasks()

        content_height = about_frame.winfo_reqheight()
        canvas_height = scroll_canvas.winfo_height()

        if content_height > canvas_height:
            if not scrollbar.winfo_manager():
                scrollbar.pack(
                    side="right",
                    fill="y"
                )
        else:
            if scrollbar.winfo_manager():
                scrollbar.pack_forget()

            scroll_canvas.yview_moveto(0)

    def update_scroll_region(event=None):
        scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")
        )

        scroll_canvas.after_idle(update_scrollbar)

    about_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    def resize_about_frame(event):
        scroll_canvas.itemconfig(
            about_window,
            width=event.width
        )

        scroll_canvas.after_idle(update_scrollbar)

    scroll_canvas.bind(
        "<Configure>",
        resize_about_frame
    )

    def mouse_wheel(event):
        if about_frame.winfo_reqheight() <= scroll_canvas.winfo_height():
            return

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
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(
        pady=(14, 8)
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
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR,
        wraplength=320,
        justify="center"
    ).pack(
        padx=20,
        pady=(0, 12)
    )

    tk.Label(
        about_frame,
        text="App Stats",
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(
        pady=(8, 10)
    )

    uptime_display = tk.StringVar()
    session_display = tk.StringVar()
    rare_display = tk.StringVar()

    tk.Label(
        about_frame,
        textvariable=uptime_display,
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack()

    tk.Label(
        about_frame,
        textvariable=session_display,
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(
        pady=(12, 0)
    )

    rare_title_frame = tk.Frame(
        about_frame,
        bg=style.BACKGROUND
    )

    rare_title_frame.pack(
        pady=(14, 0)
    )

    tk.Label(
        rare_title_frame,
        text="Rare Animations",
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
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
        padx=(6, 0)
    )

    rare_label = tk.Label(
        about_frame,
        textvariable=rare_display,
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    )

    rare_label.pack(
        pady=(2, 0)
    )

    version_label = tk.Label(
        about_frame,
        text=(
            "Version: DEV_1.0.0\n\n"
            "Created by Epicstargamer (Esg)\n"
            "Made using Python and TKinter"
        ),
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR,
        justify="center"
    )

    version_label.pack(
        pady=20
    )

    rare_details_container = tk.Frame(
        about_frame,
        bg=rare_panel_bg,
        highlightbackground=rare_border,
        highlightthickness=1,
        bd=0
    )

    rare_header = tk.Frame(
        rare_details_container,
        bg=rare_panel_bg
    )

    rare_header.pack(
        fill="x",
        padx=10,
        pady=(8, 3)
    )

    tk.Label(
        rare_header,
        text="Rare Animation Details",
        font=style.TEXT_FONT,
        bg=rare_panel_bg,
        fg=style.TEXT_COLOR
    ).pack(
        anchor="w"
    )

    rare_scroll_area = tk.Frame(
        rare_details_container,
        bg=rare_panel_bg
    )

    rare_scroll_area.pack(
        fill="both",
        expand=True,
        padx=8,
        pady=(2, 8)
    )

    rare_scrollbar = ttk.Scrollbar(
        rare_scroll_area,
        orient="vertical"
    )

    rare_scrollbar.pack(
        side="right",
        fill="y"
    )

    rare_canvas = tk.Canvas(
        rare_scroll_area,
        height=100,
        highlightthickness=0,
        bg=rare_panel_bg,
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
        bg=rare_panel_bg
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
        # Remove old rows.
        for widget in rare_list_frame.winfo_children():
            widget.destroy()

        counts = stats.get(
            "rare_animation_counts",
            {}
        )

        discovered_animations = set(
            stats.get(
                "rare_animations_discovered",
                []
            )
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

            if name in discovered_animations:
                display_name = name
            else:
                display_name = "????"

            row = tk.Frame(
                rare_list_frame,
                bg=rare_panel_bg
            )

            row.pack(
                fill="x",
                pady=2
            )

            if name in discovered_animations:
                indicator_color = "#168a28"
            else:
                indicator_color = "#c62828"

            indicator = tk.Frame(
                row,
                bg=indicator_color,
                width=4
            )

            indicator.pack(
                side="left",
                fill="y",
                padx=(0, 8)
            )

            tk.Label(
                row,
                text=display_name,
                font=style.TEXT_FONT,
                bg=rare_panel_bg,
                fg=style.TEXT_COLOR,
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

            tk.Label(
                row,
                text=f"×{count}",
                font=style.TEXT_FONT,
                bg=rare_panel_bg,
                fg=indicator_color
            ).pack(
                side="right",
                padx=(8, 2)
            )

        rare_list_frame.update_idletasks()

        rare_canvas.configure(
            scrollregion=rare_canvas.bbox("all")
        )

    def toggle_rare_details():
        if rare_details_container.winfo_manager():
            rare_details_container.pack_forget()

            update_scroll_region()

            return

        update_rare_details()

        rare_details_container.pack(
            fill="x",
            padx=20,
            pady=(7, 0),
            before=version_label
        )

        scroll_canvas.after_idle(
            update_scroll_region
        )

    rare_info.bind(
        "<Button-1>",
        lambda event: toggle_rare_details()
    )

    rare_info.bind(
        "<Enter>",
        lambda event: rare_info.config(
            fg=style.BUTTON_NORMAL
        )
    )

    rare_info.bind(
        "<Leave>",
        lambda event: rare_info.config(
            fg=style.TEXT_COLOR
        )
    )

    def update_uptime():
        nonlocal last_discovered_animations

        current_session = get_session_uptime()

        total_uptime = (
            stats.get(
                "total_uptime",
                0
            )
            + current_session
        )

        uptime_display.set(
            format_uptime(
                total_uptime
            )
        )

        session_display.set(
            f"Total Sessions:\n"
            f"{stats.get('session_count', 0)}"
        )

        discovered_animations = tuple(
            stats.get(
                "rare_animations_discovered",
                []
            )
        )

        discovered = len(
            discovered_animations
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

        if (
            rare_details_container.winfo_manager()
            and discovered_animations != last_discovered_animations
        ):
            update_rare_details()

        last_discovered_animations = discovered_animations

        rare_label.after(
            1000,
            update_uptime
        )

    update_uptime()

    scroll_canvas.after_idle(
        update_scrollbar
    )