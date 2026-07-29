import tkinter as tk
from Source.Config import style

from Source.Config.config import save_config


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
        "disable_sound",
        "Disable Sound"
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