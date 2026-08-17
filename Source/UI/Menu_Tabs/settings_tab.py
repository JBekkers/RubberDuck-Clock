import tkinter as tk
from tkinter import ttk

from Source.Config import style

from Source.Config.config import save_config
from Source.sound import set_sound_volume

from tzlocal import get_localzone_name


SETTINGS = [

    (
        "hourly_quack",
        "Hourly Quack"
    ),

    (
        "always_on_top",
        "Always On Top"
    ),

    (
        "disable_particles",
        "Disable Particles"
    )

]


# --------------------------------------------------
# Available manual timezones
# --------------------------------------------------

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


def build_settings_tab(parent, settings, config, actions):

    # ==================================================
    # SCROLLABLE SETTINGS AREA
    # ==================================================

    scroll_container = tk.Frame(
        parent
    )

    scroll_container.pack(
        fill="both",
        expand=True
    )


    # --------------------------------------------------
    # Scrollbar
    # --------------------------------------------------

    scrollbar = ttk.Scrollbar(
        scroll_container,
        orient="vertical"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # --------------------------------------------------
    # Canvas
    # --------------------------------------------------

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


    # --------------------------------------------------
    # Frame containing all settings
    # --------------------------------------------------

    settings_frame = tk.Frame(
        scroll_canvas
    )


    settings_window = scroll_canvas.create_window(
        (0, 0),
        window=settings_frame,
        anchor="nw"
    )


    # --------------------------------------------------
    # Update scroll region when content changes
    # --------------------------------------------------

    def update_scroll_region(event=None):

        scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")
        )


    settings_frame.bind(
        "<Configure>",
        update_scroll_region
    )


    # --------------------------------------------------
    # Make settings frame match canvas width
    # --------------------------------------------------

    def resize_settings_frame(event):

        scroll_canvas.itemconfig(
            settings_window,
            width=event.width
        )


    scroll_canvas.bind(
        "<Configure>",
        resize_settings_frame
    )


    # ==================================================
    # MOUSE WHEEL SCROLLING
    # ==================================================

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


    # ==================================================
    # SETTINGS TITLE
    # ==================================================

    tk.Label(
        settings_frame,
        text="Settings",
        font=style.TITLE_FONT
    ).pack(
        pady=10
    )


    # ==================================================
    # SOUND VOLUME
    # ==================================================

    tk.Label(
        settings_frame,
        text="Sound Volume",
        font=style.TEXT_FONT
    ).pack(
        pady=5
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

        set_sound_volume(
            value
        )

        save_config(
            config
        )


    tk.Scale(
        settings_frame,
        from_=0,
        to=100,
        orient="horizontal",
        variable=volume,
        command=volume_changed,
        font=style.TEXT_FONT,
        length=200,
        showvalue=True,
        highlightthickness=0
    ).pack()


    # ==================================================
    # TIME ZONE
    # ==================================================

    tk.Label(
        settings_frame,
        text="Time Zone",
        font=style.TEXT_FONT
    ).pack(
        pady=(15, 5)
    )


    # --------------------------------------------------
    # Automatic timezone setting
    # --------------------------------------------------

    auto_timezone = tk.BooleanVar(
        value=settings.get(
            "auto_timezone",
            True
        )
    )


    # --------------------------------------------------
    # Get saved timezone
    # --------------------------------------------------

    saved_timezone = settings.get(
        "timezone",
        "Europe/Amsterdam"
    )


    # --------------------------------------------------
    # Detect computer timezone
    # --------------------------------------------------

    try:

        detected_timezone = get_localzone_name()

    except Exception:

        detected_timezone = "Europe/Amsterdam"


    # --------------------------------------------------
    # Decide which timezone to display
    # --------------------------------------------------

    if auto_timezone.get():

        current_timezone = detected_timezone

    else:

        current_timezone = saved_timezone


    timezone = tk.StringVar(
        value=current_timezone
    )


    # --------------------------------------------------
    # Automatic Region Selection checkbox
    # --------------------------------------------------

    auto_timezone_check = tk.Checkbutton(
        settings_frame,
        text="Automatic Region Selection",
        font=style.TITLE_FONT,
        variable=auto_timezone
    )

    auto_timezone_check.pack(
        anchor="w",
        padx=20,
        pady=3
    )


    # --------------------------------------------------
    # Manual timezone dropdown
    # --------------------------------------------------

    timezone_dropdown = ttk.Combobox(
        settings_frame,
        textvariable=timezone,
        values=TIMEZONES,
        state=(
            "disabled"
            if auto_timezone.get()
            else "readonly"
        ),
        width=25
    )

    timezone_dropdown.pack(
        anchor="w",
        padx=40,
        pady=(0, 5)
    )


    # ==================================================
    # TIMEZONE SETTING CHANGED
    # ==================================================

    def update_timezone_setting():

        automatic = auto_timezone.get()

        settings["auto_timezone"] = automatic


        # --------------------------------------------------
        # Automatic mode
        # --------------------------------------------------

        if automatic:

            try:

                detected = get_localzone_name()

            except Exception:

                detected = "Europe/Amsterdam"


            timezone.set(
                detected
            )


            timezone_dropdown.config(
                state="disabled"
            )


        # --------------------------------------------------
        # Manual mode
        # --------------------------------------------------

        else:

            timezone.set(
                settings.get(
                    "timezone",
                    "Europe/Amsterdam"
                )
            )


            timezone_dropdown.config(
                state="readonly"
            )


        # Tell the clock that the timezone changed
        if "timezone_changed" in actions:

            actions["timezone_changed"]()


        save_config(
            config
        )


    auto_timezone_check.config(
        command=update_timezone_setting
    )


    # ==================================================
    # MANUAL TIMEZONE SELECTED
    # ==================================================

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


    # ==================================================
    # OTHER SETTINGS
    # ==================================================

    for key, text in SETTINGS:

        variable = tk.BooleanVar(
            value=settings.get(
                key,
                False
            )
        )


        def changed(
            var=variable,
            option=key
        ):

            settings[option] = var.get()


            if option in actions:

                actions[option](
                    var.get()
                )


            save_config(
                config
            )


        tk.Checkbutton(
            settings_frame,
            text=text,
            font=style.TITLE_FONT,
            variable=variable,
            command=changed
        ).pack(
            anchor="w",
            padx=20,
            pady=3
        )


    # ==================================================
    # APPLICATION
    # ==================================================

    tk.Label(
        settings_frame,
        text="Application",
        font=style.TEXT_FONT
    ).pack(
        pady=(20, 5)
    )


    # --------------------------------------------------
    # Reset Position
    # --------------------------------------------------

    tk.Button(
        settings_frame,
        text="Reset Position",
        command=actions["reset_position"],
        font=style.TITLE_FONT
    ).pack(
        pady=3
    )


    # --------------------------------------------------
    # Restart Application
    # --------------------------------------------------

    tk.Button(
        settings_frame,
        text="Restart Application",
        command=actions["restart"],
        font=style.TITLE_FONT
    ).pack(
        pady=3
    )


    # --------------------------------------------------
    # Quit Application
    # --------------------------------------------------

    tk.Button(
        settings_frame,
        text="Quit Application",
        command=actions["quit"],
        font=style.TITLE_FONT
    ).pack(
        pady=3
    )