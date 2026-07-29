import tkinter as tk
from Source.Config import style

from Source.Config.config import save_config
from Source.sound import set_sound_volume


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
        "disable_animation",
        "Disable Animations"
    ),

    (
        "disable_particles",
        "Disable Particles"
    )

]

def build_settings_tab(parent, settings, config, actions):

    tk.Label(
        parent,
        text="Settings",
        font=style.TITLE_FONT
    ).pack(pady=10)

    tk.Label(
        parent,
        text="Sound Volume",
        font=style.TEXT_FONT
    ).pack(
        pady=(5)
    )


    volume = tk.IntVar(
        value=settings.get("sound_volume", 100)
    )

    set_sound_volume(
        volume.get()
    )


    def volume_changed(value):

        value = int(float(value))

        settings["sound_volume"] = value

        set_sound_volume(value)

        save_config(config)


    tk.Scale(
        parent,
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

    for key, text in SETTINGS:

        variable = tk.BooleanVar(
            value=settings.get(key, False)
        )

        def changed(
            var=variable,
            option=key
        ):

            settings[option] = var.get()

            if option in actions:
                actions[option](var.get())

            save_config(config)

        tk.Checkbutton(
            parent,
            text=text,
            font=style.TITLE_FONT,
            variable=variable,
            command=changed
        ).pack(
            anchor="w",
            padx=20,
            pady=3
        )

    tk.Label(
        parent,
        text="Application",
        font= style.TEXT_FONT
    ).pack(
        pady=(20,5)
    )


    tk.Button(
        parent,
        text="Reset Position",
        command=actions["reset_position"],
        font=style.TITLE_FONT
    ).pack(
        pady=3
    )

    tk.Button(
        parent,
        text="Restart Application",
        command=actions["restart"],
        font=style.TITLE_FONT
    ).pack(
        pady=3
    )

    tk.Button(
        parent,
        text="Quit Application",
        command=actions["quit"],
        font=style.TITLE_FONT
    ).pack(
        pady=3
    )