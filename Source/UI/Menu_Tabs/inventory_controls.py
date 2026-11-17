
import tkinter as tk

from Source.Config import style
from Source.hats import RARITIES

def create_inventory_controls(parent, on_change, toggle_button_parent, container):

    panel = tk.Frame(
        parent,
        bg="#FFE8AD",
        highlightbackground=style.BORDER_COLOR,
        highlightthickness=1,
        bd=0
    )

    # Dropdown variables
    sort_var = tk.StringVar(value="Rarity")
    rarity_var = tk.StringVar(value="All rarities")

    filter_visible = False

    def toggle_filters():
        nonlocal filter_visible

        if filter_visible:
            panel.pack_forget()
            filter_visible = False

            filter_button.config(
                relief="flat",
                bg=style.BUTTON_NORMAL
            )

        else:
            panel.pack(
                fill="x",
                pady=(0, 9),
                before=container
            )

            filter_visible = True

            filter_button.config(
                relief="sunken",
                bg=style.BUTTON_CLICKED
            )

    # Filter icon beside Inventory heading
    filter_button = tk.Button(
        toggle_button_parent,
        text="⚙",
        command=toggle_filters,
        font=style.TEXT_FONT,
        bg=style.BUTTON_NORMAL,
        fg=style.TEXT_COLOR,
        activebackground=style.BUTTON_CLICKED,
        activeforeground=style.TEXT_COLOR,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2",
        padx=7,
        pady=2
    )

    filter_button.pack(
        side="left",
        padx=(6, 0)
    )

    # Dropdown controls
    controls = tk.Frame(
        panel,
        bg="#FFE8AD"
    )

    controls.pack(
        fill="x",
        padx=8,
        pady=(9, 8)
    )

    def create_dropdown(parent, label, variable, options):

        wrapper = tk.Frame(
            parent,
            bg="#FFE8AD"
        )

        wrapper.pack(
            side="left",
            fill="x",
            expand=True,
            padx=3
        )

        tk.Label(
            wrapper,
            text=label,
            font=style.SMALL_FONT,
            bg="#FFE8AD",
            fg=style.MUTED_TEXT
        ).pack(
            anchor="w",
            pady=(0, 3)
        )

        menu = tk.OptionMenu(
            wrapper,
            variable,
            *options,
            command=lambda value: apply_change()
        )

        menu.config(
            font=style.TEXT_FONT,
            bg=style.BUTTON_NORMAL,
            fg=style.TEXT_COLOR,
            activebackground=style.BUTTON_CLICKED,
            activeforeground=style.TEXT_COLOR,
            relief="raised",
            bd=1,
            highlightthickness=0,
            cursor="hand2",
            anchor="w",
            padx=6,
            pady=3
        )

        menu["menu"].config(
            font=style.TEXT_FONT,
            bg=style.BUTTON_NORMAL,
            fg=style.TEXT_COLOR,
            activebackground=style.BUTTON_CLICKED,
            activeforeground=style.TEXT_COLOR,
            bd=0,
            activeborderwidth=0
        )

        menu.pack(fill="x")

        menu.bind(
            "<Enter>",
            lambda event: menu.config(
                bg=style.BUTTON_CLICKED
            )
        )

        menu.bind(
            "<Leave>",
            lambda event: menu.config(
                bg=style.BUTTON_NORMAL
            )
        )

    # Summary
    footer = tk.Frame(
        panel,
        bg="#FFE8AD"
    )

    footer.pack(
        fill="x",
        padx=9,
        pady=(0, 6)
    )

    summary = tk.Label(
        footer,
        text="All rarities • Rarity",
        font=style.SMALL_FONT,
        bg="#FFE8AD",
        fg=style.MUTED_TEXT
    )

    summary.pack(side="left")

    def update_summary():

        sort_text = sort_var.get()
        rarity_text = rarity_var.get()

        if rarity_text == "All rarities":
            summary.config(
                text=f"All rarities • {sort_text}"
            )
        else:
            summary.config(
                text=f"{rarity_text} only • {sort_text}"
            )

    def apply_change():
        update_summary()
        on_change()

    # Sorting dropdown
    create_dropdown(
        controls,
        "SORT BY",
        sort_var,
        [
            "Rarity",
            "Newest",
            "Oldest",
            "A-Z",
            "Z-A"
        ]
    )

    # Rarity dropdown
    create_dropdown(
        controls,
        "RARITY",
        rarity_var,
        [
            "All rarities",
            *RARITIES.keys()
        ]
    )

    # Reset button
    def reset_filters():
        sort_var.set("Rarity")
        rarity_var.set("All rarities")
        apply_change()

    reset_button = tk.Button(
        footer,
        text="Reset",
        command=reset_filters,
        font=style.SMALL_FONT,
        bg=style.BUTTON_NORMAL,
        fg=style.TEXT_COLOR,
        activebackground=style.BUTTON_CLICKED,
        activeforeground=style.TEXT_COLOR,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2",
        padx=8,
        pady=2
    )

    reset_button.pack(side="right")

    reset_button.bind(
        "<Enter>",
        lambda event: reset_button.config(
            bg=style.BUTTON_CLICKED
        )
    )

    reset_button.bind(
        "<Leave>",
        lambda event: reset_button.config(
            bg=style.BUTTON_NORMAL
        )
    )

    return sort_var, rarity_var

def get_filtered_inventory(hat_manager, sort_mode, rarity_filter):
    owned = list(hat_manager.owned)

    if sort_mode == "Rarity":
        owned = hat_manager.get_sorted_inventory()
    elif sort_mode == "Newest":
        owned.reverse()
    elif sort_mode == "Oldest":
        pass
    elif sort_mode == "A-Z":
        owned.sort(
            key=lambda item: hat_manager.catalog[item["hat_id"]]["name"].casefold()
        )
    elif sort_mode == "Z-A":
        owned.sort(
            key=lambda item: hat_manager.catalog[item["hat_id"]]["name"].casefold(),
            reverse=True
        )

    if rarity_filter != "All rarities":
        owned = [
            item for item in owned
            if hat_manager.catalog[item["hat_id"]]["rarity"] == rarity_filter
        ]

    return owned
