import tkinter as tk
from tkinter import ttk

from Source.Config import style
from Source.Config.config import save_config
from Source.sound import set_sound_volume, play_sound

from tzlocal import get_localzone_name

# ==================================================
# BUTTON HOVER EFFECT
# ==================================================

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

# ==================================================
# SECTION TITLE
# ==================================================

def section_title(parent, text):

    tk.Label(
        parent,
        text=text,
        font=style.TEXT_FONT
    ).pack(
        pady=(15, 5)
    )


# ==================================================
# SOUND SETTINGS
# ==================================================

SOUND_SETTINGS = [

    (
        "clock_24_hour",
        "24 Hour Clock"
    ),

    (
        "hourly_quack",
        "Hourly Quack"
    )

]


# ==================================================
# OTHER SETTINGS
# ==================================================

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


# ==================================================
# AVAILABLE MANUAL TIMEZONES
# ==================================================

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


# ==================================================
# BUILD SETTINGS TAB
# ==================================================

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


    # ==================================================
    # SCROLLBAR
    # ==================================================

    scrollbar_style = ttk.Style()

    scrollbar_style.theme_use(
        "clam"
    )

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


    # ==================================================
    # CANVAS
    # ==================================================

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


    # ==================================================
    # SETTINGS FRAME
    # ==================================================

    settings_frame = tk.Frame(
        scroll_canvas
    )

    settings_window = scroll_canvas.create_window(
        (0, 0),
        window=settings_frame,
        anchor="nw"
    )


    # ==================================================
    # UPDATE SCROLL REGION
    # ==================================================

    def update_scroll_region(event=None):

        scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")
        )


    settings_frame.bind(
        "<Configure>",
        update_scroll_region
    )


    # ==================================================
    # MATCH FRAME WIDTH TO CANVAS
    # ==================================================

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
    # MOUSE WHEEL
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
    # MAIN SETTINGS TITLE
    # ==================================================

    tk.Label(
        settings_frame,
        text="Settings",
        font=style.TITLE_FONT
    ).pack(
        pady=10
    )


    # ==================================================
    # SOUND SETTINGS
    # ==================================================

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


    # ==================================================
    # VOLUME CHANGED
    # ==================================================

    def volume_changed(value):

        value = int(
            float(value)
        )

        settings["sound_volume"] = value

        set_sound_volume(
            value
        )

        volume_display.set(
            f"{value}%"
        )

        save_config(
            config
        )


    # ==================================================
    # VOLUME RELEASED
    # ==================================================

    def volume_released(event):

        play_sound(
            "quack.wav"
        )


    # ==================================================
    # VOLUME CONTAINER
    # ==================================================

    volume_container = tk.Frame(
        settings_frame
    )

    volume_container.pack(
        fill="x",
        pady=(3)
    )

    volume_container.configure(
        height=35
    )

    volume_container.pack_propagate(
        False
    )


    # ==================================================
    # VOLUME SLIDER
    # ==================================================

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


    # ==================================================
    # VOLUME PERCENTAGE
    # ==================================================

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
        x= 108,
        anchor="w"
    )


    # ==================================================
    # CLICK ANYWHERE ON SLIDER
    # ==================================================

    def slider_clicked(event):

        # Current thumb position
        thumb_x = volume_scale.coords(
            volume_scale.get()
        )[0]

        # Approximate half the thumb width
        thumb_half_width = (
            volume_scale.cget("sliderlength") / 2
        )

        # If clicking the thumb,
        # let Tkinter handle normal dragging.
        if (
            thumb_x - thumb_half_width
            <= event.x
            <=
            thumb_x + thumb_half_width
        ):
            return


        # Actual slider range
        min_x = volume_scale.coords(
            volume_scale.cget("from")
        )[0]

        max_x = volume_scale.coords(
            volume_scale.cget("to")
        )[0]


        # Keep click inside slider
        x = max(
            min_x,
            min(
                event.x,
                max_x
            )
        )


        # Convert position to percentage
        percentage = (
            (x - min_x)
            /
            (max_x - min_x)
        )


        value = round(
            percentage * 100
        )


        # Move slider
        volume_scale.set(
            value
        )


        # Update volume
        volume_changed(
            value
        )


    volume_scale.bind(
        "<Button-1>",
        slider_clicked,
        add="+"
    )


    volume_scale.bind(
        "<ButtonRelease-1>",
        volume_released
    )


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


    # ==================================================
    # AUTOMATIC TIMEZONE
    # ==================================================

    auto_timezone = tk.BooleanVar(
        value=settings.get(
            "auto_timezone",
            True
        )
    )


    # ==================================================
    # SAVED TIMEZONE
    # ==================================================

    saved_timezone = settings.get(
        "timezone",
        "Europe/Amsterdam"
    )


    # ==================================================
    # DETECT COMPUTER TIMEZONE
    # ==================================================

    try:

        detected_timezone = get_localzone_name()

    except Exception:

        detected_timezone = "Europe/Amsterdam"


    # ==================================================
    # DETERMINE CURRENT TIMEZONE
    # ==================================================

    if auto_timezone.get():

        current_timezone = detected_timezone

    else:

        current_timezone = saved_timezone


    timezone = tk.StringVar(
        value=current_timezone
    )


    # ==================================================
    # TIMEZONE CONTROLS
    # ==================================================

    timezone_controls = tk.Frame(
        settings_frame
    )

    timezone_controls.pack(
        fill="x"
    )


    # ==================================================
    # AUTOMATIC REGION SELECTION
    # ==================================================

    auto_timezone_check = tk.Checkbutton(
        timezone_controls,
        text="Automatic Region Selection",
        font=style.TITLE_FONT,
        variable=auto_timezone
    )

    auto_timezone_check.pack(
        anchor="w",
        padx=20,
        pady=3
    )


    # ==================================================
    # TIMEZONE DROPDOWN STYLE
    # ==================================================

    dropdown_style = ttk.Style()

    dropdown_style.theme_use(
        "clam"
    )

    dropdown_style.configure(
        "Settings.TCombobox",
        fieldbackground=style.BACKGROUND,
        background=style.BUTTON_NORMAL,
        foreground=style.TEXT_COLOR,
        arrowcolor=style.TEXT_COLOR
    )


    # ==================================================
    # TIMEZONE DROPDOWN
    # ==================================================

    timezone_dropdown = ttk.Combobox(
        timezone_controls,
        textvariable=timezone,
        values=TIMEZONES,
        state="readonly",
        width=25,
        style="Settings.TCombobox"
    )


    # ==================================================
    # TIMEZONE CHANGED
    # ==================================================

    def update_timezone_setting():

        automatic = auto_timezone.get()

        settings["auto_timezone"] = automatic


        # ==================================================
        # AUTOMATIC MODE
        # ==================================================

        if automatic:

            try:

                detected = get_localzone_name()

            except Exception:

                detected = "Europe/Amsterdam"


            timezone.set(
                detected
            )


            timezone_dropdown.pack_forget()


        # ==================================================
        # MANUAL MODE
        # ==================================================

        else:

            timezone.set(
                settings.get(
                    "timezone",
                    "Europe/Amsterdam"
                )
            )


            timezone_dropdown.pack(
                anchor="w",
                padx=20,
                pady=3
            )


        # Tell clock that timezone changed
        if "timezone_changed" in actions:

            actions["timezone_changed"]()


        save_config(
            config
        )


    auto_timezone_check.config(
        command=update_timezone_setting
    )


    # ==================================================
    # SHOW DROPDOWN INITIALLY IF MANUAL MODE
    # ==================================================

    if not auto_timezone.get():

        timezone_dropdown.pack(
            anchor="w",
            padx=20,
            pady=3
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
    # SOUND SETTINGS OPTIONS
    # ==================================================

    for key, text in SOUND_SETTINGS:

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
    # OTHER SETTINGS
    # ==================================================

    section_title(
        settings_frame,
        "Other Settings"
    )


    for key, text in OTHER_SETTINGS:

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

    section_title(
        settings_frame,
        "Application"
    )


    # ==================================================
    # APPLICATION BUTTONS
    # ==================================================

    #reset
    reset_button = tk.Button(
        settings_frame,
        text="Reset Clock Position",
        command=actions["reset_position"],
        font=style.TITLE_FONT,
        bg=style.BUTTON_NORMAL,
        activebackground=style.BUTTON_CLICKED
    )

    reset_button.pack(
        pady=3
    )

    add_button_hover(
        reset_button
    )

    #restart
    restart_button = tk.Button(
        settings_frame,
        text="Restart Application",
        command=actions["restart"],
        font=style.TITLE_FONT,
        bg=style.BUTTON_NORMAL,
        activebackground=style.BUTTON_CLICKED
    )

    restart_button.pack(
        pady=3
    )

    add_button_hover(
        restart_button
    )


    #quit
    quit_button = tk.Button(
        settings_frame,
        text="Quit Application",
        command=actions["quit"],
        font=style.TITLE_FONT,
        bg=style.BUTTON_NORMAL,
        activebackground=style.BUTTON_CLICKED
    )

    quit_button.pack(
        pady=3
    )

    add_button_hover(
        quit_button
    )