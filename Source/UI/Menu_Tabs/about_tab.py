import tkinter as tk

from Source.Config import style
from Source.animation import animations, set_rare_animation_callback
from Source.Config.scrollbar import FlatScrollbar

def format_uptime(seconds):
    hours = seconds / 3600
    return f"Total Uptime:\n{hours:.1f} hours"

def build_about_tab(parent, settings, config, stats):
    scroll_container = tk.Frame(parent)

    scroll_container.pack(
        fill="both",
        expand=True
    )

    scroll_canvas = tk.Canvas(
        scroll_container,
        highlightthickness=0,
        bg=style.BACKGROUND,
        bd=0
    )

    scrollbar_frame = tk.Frame(
        scroll_container,
        width=style.SCROLLBAR_WIDTH,
        bg=style.BACKGROUND
    )

    scrollbar_frame.pack(
        side="right",
        fill="y"
    )

    scrollbar_frame.pack_propagate(False)

    scrollbar = FlatScrollbar(
        scrollbar_frame,
        command=scroll_canvas.yview
    )

    scrollbar.pack(
        fill="y",
        expand=True
    )

    scroll_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scroll_canvas.configure(
        yscrollcommand=scrollbar.set
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

    rare_panel_bg = style.RARE_PANEL_BACKGROUND
    rare_border = style.RARE_PANEL_BORDER

    def update_scrollbar():
        scroll_canvas.update_idletasks()
        about_frame.update_idletasks()

        content_height = about_frame.winfo_reqheight()
        canvas_height = scroll_canvas.winfo_height()

        if content_height > canvas_height:
            scrollbar_frame.configure(
                width=style.SCROLLBAR_WIDTH
            )
        else:
            scrollbar_frame.configure(
                width=0
            )

            scroll_canvas.yview_moveto(0)

        scroll_container.update_idletasks()

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
        wraplength=style.ABOUT_TEXT_WRAP_LENGTH,
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

    def update_rare_summary():
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

    session_display.set(
        f"Total Sessions:\n"
        f"{stats.get('session_count', 0)}"
    )

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

    update_rare_summary()

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
        height=style.RARE_PANEL_HEIGHT,
        bg=rare_panel_bg,
        highlightbackground=rare_border,
        highlightthickness=style.RARE_PANEL_BORDER_WIDTH,
        bd=0
    )

    rare_details_container.pack_propagate(False)

    rare_header = tk.Frame(
        rare_details_container,
        bg=rare_panel_bg
    )

    rare_header.pack(
        fill="x",
        padx=10,
        pady=(5, 2)
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
        pady=(2, 5)
    )

    rare_canvas = tk.Canvas(
        rare_scroll_area,
        highlightthickness=0,
        bg=rare_panel_bg,
        bd=0
    )

    rare_scrollbar = FlatScrollbar(
        rare_scroll_area,
        command=rare_canvas.yview,
        bg=rare_panel_bg,
        width=style.RARE_SCROLLBAR_WIDTH,
        thumb_color=style.SCROLLBAR_THUMB,
        hover_color=style.SCROLLBAR_THUMB_HOVER,
        thumb_width=style.RARE_SCROLLBAR_THUMB_WIDTH,
        thumb_height=style.RARE_SCROLLBAR_THUMB_HEIGHT
    )

    rare_scrollbar.pack(
        side="right",
        fill="y"
    )

    rare_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    rare_canvas.configure(
        yscrollcommand=rare_scrollbar.set
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
                indicator_color = style.UNLOCKED_COLOR
            else:
                display_name = "????"
                indicator_color = style.LOCKED_COLOR

            row = tk.Frame(
                rare_list_frame,
                bg=rare_panel_bg
            )

            row.pack(
                fill="x",
                pady=2
            )

            indicator = tk.Frame(
                row,
                bg=indicator_color,
                width=style.RARE_INDICATOR_WIDTH
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

    def refresh_rare_details():
        if not rare_details_container.winfo_exists():
            return

        update_rare_summary()

        if rare_details_container.winfo_manager():
            update_rare_details()
            update_scroll_region()

    set_rare_animation_callback(
        refresh_rare_details
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
        total_uptime = stats.get(
            "total_uptime",
            0
        )

        uptime_display.set(
            format_uptime(total_uptime)
        )

        rare_label.after(
            60000,
            update_uptime
        )

    update_uptime()

    scroll_canvas.after_idle(
        update_scrollbar
    )