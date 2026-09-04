import tkinter as tk
from tkinter import ttk
from Source.Config import style
from Source.Config.config import save_config
from Source.sound import set_sound_volume, play_sound
from tzlocal import get_localzone_name


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
        font=style.TEXT_FONT,
    ).pack(
        pady=(15, 5)
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
        return DEFAULT_TIMEZONE
    
def build_settings_tab(parent, settings, config, actions):


    scroll_container = tk.Frame(parent)
    scroll_container.pack(fill="both",expand=True)

    scrollbar_style = ttk.Style()
    scrollbar_style.theme_use("clam")

    scrollbar_style.configure(
        "Settings.Vertical.TScrollbar",
        background=style.SCROLL_BACKGROUND,
        troughcolor=style.SCROLL_TROUGH,
        bordercolor=style.SCROLL_BORDER,
        arrowcolor=style.SCROLL_ARROW,
        relief="flat",
        width=14
    )

    scrollbar_style.map(
        "Settings.Vertical.TScrollbar",

        background=[
            ("active", style.BUTTON_CLICKED),
            ("pressed", style.BUTTON_CLICKED)
        ]
    )


    scrollbar = ttk.Scrollbar(
        scroll_container,
        orient="vertical",
        style="Settings.Vertical.TScrollbar"
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


    scrollbar.config(command=scroll_canvas.yview)

    settings_frame = tk.Frame(scroll_canvas)


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
            font=style.TITLE_FONT,
            variable=variable,
            bg=style.BACKGROUND,
            activebackground=style.BACKGROUND,
            selectcolor=style.BACKGROUND,
            fg="black",
            activeforeground="black",
            command=changed
        ).pack(
            anchor="w",
            padx=20,
            pady=3
        )

    def update_scroll_region(event=None):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))


    settings_frame.bind("<Configure>",update_scroll_region)

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
        scroll_canvas.yview_scroll(int(-1 *(event.delta / 120)),"units")

    def enable_mousewheel(event):
        scroll_canvas.bind_all("<MouseWheel>",mouse_wheel)

    def disable_mousewheel(event):
        scroll_canvas.unbind_all("<MouseWheel>")

    scroll_canvas.bind(  "<Enter>",enable_mousewheel)
    scroll_canvas.bind("<Leave>",disable_mousewheel
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

    volume_display = tk.StringVar(
        value=f"{volume.get()}%"
    )

    set_sound_volume(
        volume.get()
    )

    def volume_changed(value):

        value = int(float(value))
        settings["sound_volume"] = value
        set_sound_volume(value)
        volume_display.set(f"{value}%")
        save_config(config)


    def volume_released(event):
        play_sound("quack.wav" )

    volume_container = tk.Frame(settings_frame)
    volume_container.pack(fill="x",pady=3)
    volume_container.configure(height=35)
    volume_container.pack_propagate(False)

    volume_scale = tk.Scale(
        volume_container,
        from_=0,
        to=100,
        orient="horizontal",
        variable=volume,
        command=volume_changed,
        font=style.TEXT_FONT,
        length=200,
        showvalue=False,
        highlightthickness=0,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR,
        troughcolor=style.BUTTON_NORMAL,
        activebackground=style.BUTTON_CLICKED,
        sliderlength=25,
        width=12
    )

    volume_scale.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    volume_display_label = tk.Label(
        volume_container,
        textvariable=volume_display,
        font=style.TEXT_FONT,
        width=5,
        anchor="w"
    )


    volume_display_label.place(
        relx=0.5,
        rely=0.5,
        x=108,
        anchor="w"
    )

    def slider_clicked(event):

        thumb_x = volume_scale.coords(
            volume_scale.get()
        )[0]

        thumb_half_width = (
            volume_scale.cget("sliderlength")/2
        )

        if (thumb_x - thumb_half_width <= event.x <= thumb_x + thumb_half_width):
            return

        min_x = volume_scale.coords(volume_scale.cget("from"))[0]
        max_x = volume_scale.coords(volume_scale.cget("to"))[0]
        x = max(min_x,min(event.x,max_x))
        percentage = ((x - min_x)/(max_x - min_x))
        value = round(percentage * 100)
        volume_scale.set(value)
        volume_changed(value)

    volume_scale.bind("<Button-1>",slider_clicked,add="+")
    volume_scale.bind("<ButtonRelease-1>",volume_released)

    # ==================================================
    # CLOCK SETTINGS
    # ==================================================

    tk.Label(
        settings_frame,
        text="Clock settings",
        font=style.TEXT_FONT
    ).pack(
        pady=(15, 5)
    )


    auto_timezone = tk.BooleanVar(value=settings.get("auto_timezone",True))
    saved_timezone = settings.get("timezone","Europe/Amsterdam")

    detected_timezone = get_detected_timezone()

    def update_timezone_dropdown():
        timezone_dropdown.config(
            state="disabled" if auto_timezone.get() else "readonly"
        )

    if auto_timezone.get():
        current_timezone = detected_timezone

    else:
        current_timezone = saved_timezone

    timezone = tk.StringVar(value=current_timezone)
    timezone_controls = tk.Frame(settings_frame)
    timezone_controls.pack(fill="x")

    auto_timezone_check = tk.Checkbutton(
        timezone_controls,
        text="Automatic Region Selection",
        font=style.TITLE_FONT,
        variable=auto_timezone,
        bg=style.BACKGROUND,
        activebackground=style.BACKGROUND,
        selectcolor=style.BACKGROUND,
        fg="black",
        activeforeground="black"
    )

    auto_timezone_check.pack(
        anchor="w",
        padx=20,
        pady=3
    )

    dropdown_style = ttk.Style()

    dropdown_style.theme_use("clam")

    dropdown_style.configure(
        "Settings.TCombobox",
        fieldbackground=style.BUTTON_NORMAL,
        background=style.BUTTON_NORMAL,
        foreground="black",
        arrowcolor="black",
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
                "#d0d0d0"
            )
        ],

        background=[
            (
                "readonly",
                style.BUTTON_NORMAL
            ),

            (
                "disabled",
                "#d0d0d0"
            )
        ],

        foreground=[
            (
                "readonly",
                "black"
            ),

            (
                "disabled",
                "#777777"
            )
        ],

        bordercolor=[
            (
                "readonly",
                style.BUTTON_NORMAL
            ),

            (
                "disabled",
                "#d0d0d0"
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
                "black"
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
        width=25,
        style="Settings.TCombobox"
    )

    timezone_dropdown.pack(
        anchor="w",
        padx=(45,20),
        pady=3
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
            selected = settings.get("timezone",DEFAULT_TIMEZONE)

            if selected not in TIMEZONES:
                selected = DEFAULT_TIMEZONE

            timezone.set(selected)

        update_timezone_dropdown()


        if "timezone_changed" in actions:
            actions["timezone_changed"]()

        save_config(config)

    update_timezone_dropdown()
    auto_timezone_check.config(command=update_timezone_setting)

    for key, text in SOUND_SETTINGS:
        add_setting_checkbox(
            settings_frame,
            settings,
            config,
            actions,
            key,
            text
        )

    section_title(settings_frame, "Other Settings")


    for key, text in OTHER_SETTINGS:
        add_setting_checkbox(
            settings_frame,
            settings,
            config,
            actions,
            key,
            text
        )

    section_title(settings_frame,"Application")

    def add_action_button(parent, text, command):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=style.TITLE_FONT,
            bg=style.BUTTON_NORMAL,
            fg="black",
            activeforeground="black",
            activebackground=style.BUTTON_CLICKED
        )

        button.pack(pady=3)
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