import tkinter as tk
from tkinter import ttk
from Source.Config import style
from Source.Config.config import save_config
from Source.Config.scrollbar import FlatScrollbar
from Source.sound import set_sound_volume, play_sound
from tzlocal import get_localzone_name

from Source.Config.error_handler import logger

def add_button_hover(button):
    button.bind(
        "<Enter>",
        lambda event: button.config(
            bg=style.BUTTON_CLICKED
        )
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(
            bg=style.BUTTON_NORMAL
        )
    )

def section_title(parent, text):
    tk.Label(
        parent,
        text=text,
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(
        pady=(18, 8)
    )

SOUND_SETTINGS = [
    (
        "clock_24_hour",
        "24 Hour Clock"
    ),
    (
        "hourly_quack",
        "Hourly Quack Alarm"
    )
]

OTHER_SETTINGS = [
    (
        "always_on_top",
        "Always On Top"
    ),
    (
        "disable_particles",
        "Disable Particles"
    )
]

TIMEZONES = sorted([
    "Africa/Cairo",
    "Africa/Johannesburg",

    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "America/New_York",
    "America/Sao_Paulo",

    "Asia/Bangkok",
    "Asia/Dubai",
    "Asia/Hong_Kong",
    "Asia/Jakarta",
    "Asia/Kolkata",
    "Asia/Seoul",
    "Asia/Shanghai",
    "Asia/Singapore",
    "Asia/Tokyo",

    "Australia/Adelaide",
    "Australia/Brisbane",
    "Australia/Melbourne",
    "Australia/Perth",
    "Australia/Sydney",

    "Europe/Amsterdam",
    "Europe/Athens",
    "Europe/Berlin",
    "Europe/Brussels",
    "Europe/Dublin",
    "Europe/Helsinki",
    "Europe/Istanbul",
    "Europe/Lisbon",
    "Europe/London",
    "Europe/Madrid",
    "Europe/Moscow",
    "Europe/Paris",
    "Europe/Prague",
    "Europe/Rome",
    "Europe/Stockholm",
    "Europe/Vienna",

    "Pacific/Auckland",
    "Pacific/Honolulu",
])

DEFAULT_TIMEZONE = "Europe/Amsterdam"

def get_detected_timezone():
    try:
        return get_localzone_name()
    except Exception:
        logger.exception(
            "Failed to detect local timezone."
        )
        return DEFAULT_TIMEZONE

def build_settings_tab(parent, settings, config, actions):
    scroll_container = tk.Frame(
        parent,
        bg=style.BACKGROUND
    )

    scroll_container.pack(
        fill="both",
        expand=True
    )

    scroll_canvas = tk.Canvas(
        scroll_container,
        bg=style.BACKGROUND,
        highlightthickness=0,
        bd=0
    )

    scroll_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = FlatScrollbar(
        scroll_container,
        command=scroll_canvas.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    scroll_canvas.configure(
        yscrollcommand=scrollbar.set
    )

    settings_frame = tk.Frame(
        scroll_canvas,
        bg=style.BACKGROUND
    )

    settings_window = scroll_canvas.create_window(
        (0, 0),
        window=settings_frame,
        anchor="nw"
    )

    def add_setting_checkbox(parent, settings, config, actions, key, text):
        variable = tk.BooleanVar(value=settings.get(key, False))

        def changed():
            value = variable.get()
            settings[key] = value

            if key in actions:
                actions[key](value)

            save_config(config)

        tk.Checkbutton(
            parent,
            text=text,
            font=style.TEXT_FONT,
            variable=variable,
            bg=style.BACKGROUND,
            activebackground=style.BACKGROUND,
            selectcolor=style.BACKGROUND,
            fg=style.TEXT_COLOR,
            activeforeground=style.TEXT_COLOR,
            command=changed
        ).pack(
            anchor="w",
            padx=style.CONTROL_PADDING_X,
            pady=style.CONTROL_PADDING_Y
        )

    def update_scroll_region(event=None):
        scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")
        )

    settings_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    def resize_settings_frame(event):
        scroll_canvas.itemconfig(
            settings_window,
            width=event.width
        )

    scroll_canvas.bind(
        "<Configure>",
        resize_settings_frame
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
        settings_frame,
        text="Settings",
        font=style.TITLE_FONT
    ).pack(
        pady=10
    )

    tk.Label(
        settings_frame,
        text="Volume",
        font=style.TEXT_FONT
    ).pack(
        pady=0
    )

    volume = tk.IntVar(
        value=settings.get(
            "sound_volume",
            100
        )
    )

    set_sound_volume(
        volume.get()
    )

    def volume_changed(value):
        value = int(float(value))
        settings["sound_volume"] = value
        set_sound_volume(value)
        save_config(config)

    def volume_released(event):
        play_sound("quack.wav")

    volume_container = tk.Frame(
        settings_frame,
        bg=style.BACKGROUND,
        height=style.VOLUME_CONTAINER_HEIGHT
    )

    volume_container.pack(
        fill="x",
        pady=style.VOLUME_CONTAINER_PADDING_Y
    )

    volume_container.pack_propagate(False)

    volume_canvas = tk.Canvas(
        volume_container,
        width=style.VOLUME_CANVAS_WIDTH,
        height=style.VOLUME_CANVAS_HEIGHT,
        bg=style.BACKGROUND,
        highlightthickness=0,
        bd=0
    )

    volume_canvas.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    track_start = 34
    track_end = 240
    track_y = style.VOLUME_CANVAS_HEIGHT // 2
    thumb_radius = style.VOLUME_THUMB_RADIUS

    def draw_volume_slider():
        volume_canvas.delete("all")

        volume_canvas.create_line(
            track_start,
            track_y,
            track_end,
            track_y,
            fill=style.VOLUME_TRACK_COLOR,
            width=style.VOLUME_TRACK_HEIGHT,
            capstyle="round"
        )

        percentage = volume.get() / 100

        thumb_x = (
            track_start
            + percentage * (track_end - track_start)
        )

        volume_canvas.create_oval(
            thumb_x - thumb_radius + 1,
            track_y - thumb_radius + 2,
            thumb_x + thumb_radius + 1,
            track_y + thumb_radius + 2,
            fill="#D7CBBE",
            outline=""
        )

        volume_canvas.create_oval(
            thumb_x - thumb_radius,
            track_y - thumb_radius,
            thumb_x + thumb_radius,
            track_y + thumb_radius,
            fill=style.VOLUME_THUMB_COLOR,
            outline=""
        )

        volume_canvas.create_text(
            13,
            track_y,
            text="◖",
            fill=style.VOLUME_ICON_COLOR
        )

        volume_canvas.create_text(
            260,
            track_y,
            text="◖))",
            fill=style.VOLUME_ICON_COLOR
        )

    def set_volume_from_mouse(event):
        x = max(
            track_start,
            min(event.x, track_end)
        )

        percentage = (
            (x - track_start)
            / (track_end - track_start)
        )

        value = round(percentage * 100)

        if value != volume.get():
            volume.set(value)
            volume_changed(value)

        draw_volume_slider()

    volume_canvas.bind(
        "<Button-1>",
        set_volume_from_mouse
    )

    volume_canvas.bind(
        "<B1-Motion>",
        set_volume_from_mouse
    )

    volume_canvas.bind(
        "<ButtonRelease-1>",
        volume_released
    )

    draw_volume_slider()

    tk.Label(
        settings_frame,
        text="Clock settings",
        font=style.TITLE_FONT
    ).pack(
        pady=(15, 5)
    )

    auto_timezone = tk.BooleanVar(
        value=settings.get(
            "auto_timezone",
            True
        )
    )

    saved_timezone = settings.get(
        "timezone",
        "Europe/Amsterdam"
    )

    detected_timezone = get_detected_timezone()

    def update_timezone_dropdown():
        timezone_dropdown.config(
            state="disabled" if auto_timezone.get() else "readonly"
        )

    if auto_timezone.get():
        current_timezone = detected_timezone
    else:
        current_timezone = saved_timezone

    timezone = tk.StringVar(
        value=current_timezone
    )

    timezone_controls = tk.Frame(
        settings_frame
    )

    timezone_controls.pack(
        fill="x"
    )

    auto_timezone_check = tk.Checkbutton(
        timezone_controls,
        text="Automatic Region Selection",
        font=style.TEXT_FONT,
        variable=auto_timezone,
        bg=style.BACKGROUND,
        activebackground=style.BACKGROUND,
        selectcolor=style.BACKGROUND,
        fg=style.TEXT_COLOR,
        activeforeground=style.TEXT_COLOR
    )

    auto_timezone_check.pack(
        anchor="w",
        padx=style.CONTROL_PADDING_X,
        pady=style.CONTROL_PADDING_Y
    )

    dropdown_style = ttk.Style()
    dropdown_style.theme_use("clam")

    dropdown_style.configure(
        "Settings.TCombobox",
        fieldbackground=style.BUTTON_NORMAL,
        background=style.BUTTON_NORMAL,
        foreground=style.TEXT_COLOR,
        arrowcolor=style.TEXT_COLOR,
        bordercolor=style.BUTTON_NORMAL,
        lightcolor=style.BUTTON_NORMAL,
        darkcolor=style.BUTTON_NORMAL
    )

    dropdown_style.map(
        "Settings.TCombobox",
        fieldbackground=[
            (
                "readonly",
                style.BUTTON_NORMAL
            ),
            (
                "disabled",
                style.DISABLED_BACKGROUND
            )
        ],
        background=[
            (
                "readonly",
                style.BUTTON_NORMAL
            ),
            (
                "disabled",
                style.DISABLED_BACKGROUND
            )
        ],
        foreground=[
            (
                "readonly",
                style.TEXT_COLOR
            ),
            (
                "disabled",
                style.DISABLED_TEXT
            )
        ],
        bordercolor=[
            (
                "readonly",
                style.BUTTON_NORMAL
            ),
            (
                "disabled",
                style.DISABLED_BACKGROUND
            )
        ],
        lightcolor=[
            (
                "readonly",
                style.BUTTON_NORMAL
            )
        ],
        darkcolor=[
            (
                "readonly",
                style.BUTTON_NORMAL
            )
        ],
        arrowcolor=[
            (
                "readonly",
                style.TEXT_COLOR
            ),
            (
                "disabled",
                "#777777"
            )
        ]
    )

    timezone_dropdown = ttk.Combobox(
        timezone_controls,
        textvariable=timezone,
        values=TIMEZONES,
        state="readonly",
        width=style.TIMEZONE_WIDTH,
        style="Settings.TCombobox"
    )

    timezone_dropdown.pack(
        anchor="w",
        padx=(
            style.TIMEZONE_PADDING_LEFT,
            style.TIMEZONE_PADDING_RIGHT
        ),
        pady=style.CONTROL_PADDING_Y
    )

    def timezone_selected(event=None):
        settings["timezone"] = timezone.get()

        if "timezone_changed" in actions:
            actions["timezone_changed"]()

        save_config(
            config
        )

    timezone_dropdown.bind(
        "<<ComboboxSelected>>",
        timezone_selected
    )

    def update_timezone_setting():
        automatic = auto_timezone.get()
        settings["auto_timezone"] = automatic

        if automatic:
            detected = get_detected_timezone()
            timezone.set(detected)
        else:
            selected = settings.get(
                "timezone",
                DEFAULT_TIMEZONE
            )

            if selected not in TIMEZONES:
                selected = DEFAULT_TIMEZONE

            timezone.set(selected)

        update_timezone_dropdown()

        if "timezone_changed" in actions:
            actions["timezone_changed"]()

        save_config(config)

    update_timezone_dropdown()
    auto_timezone_check.config(
        command=update_timezone_setting
    )

    for key, text in SOUND_SETTINGS:
        add_setting_checkbox(
            settings_frame,
            settings,
            config,
            actions,
            key,
            text
        )

    section_title(
        settings_frame,
        "Other Settings"
    )

    for key, text in OTHER_SETTINGS:
        add_setting_checkbox(
            settings_frame,
            settings,
            config,
            actions,
            key,
            text
        )

    section_title(
        settings_frame,
        "Application"
    )

    def add_action_button(parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=style.TITLE_FONT,
            bg=style.BUTTON_NORMAL,
            fg=style.TEXT_COLOR,
            activeforeground=style.TEXT_COLOR,
            activebackground=style.BUTTON_CLICKED
        )

        button.pack(
            pady=style.BUTTON_PADDING_Y
        )

        add_button_hover(button)

    add_action_button(
        settings_frame,
        "Reset Clock Position",
        actions["reset_position"]
    )

    add_action_button(
        settings_frame,
        "Restart Application",
        actions["restart"]
    )

    add_action_button(
        settings_frame,
        "Quit Application",
        actions["quit"]
    )