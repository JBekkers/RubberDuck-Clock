
import tkinter as tk

from Source.Config import style
from Source.hats import RARITIES
from Source.Config.config import save_config
from Source.Config.paths import UI_DIR
import os

def create_inventory_controls(
    parent,
    on_change,
    toggle_button_parent,
    container,
    config,
    filter_key
):

    panel = tk.Frame(
        parent,
        bg="#FFE8AD",
        highlightbackground=style.BORDER_COLOR,
        highlightthickness=1,
        bd=0
    )

    # Load previously saved filter preferences
    saved_filters = config.setdefault(
        "settings", {}
    ).get(filter_key, {})

    if not isinstance(saved_filters, dict):
        saved_filters = {}

    saved_sort = saved_filters.get("sort", "Rarity")

    if saved_sort not in [
        "Rarity", "Newest", "Oldest", "A-Z", "Z-A"
    ]:
        saved_sort = "Rarity"

    saved_rarities = saved_filters.get("rarities", [])

    if not isinstance(saved_rarities, list):
        saved_rarities = []

    sort_var = tk.StringVar(value=saved_sort)

    if "rarities" not in saved_filters:
        saved_rarities = list(RARITIES)

    rarity_vars = {
        rarity: tk.BooleanVar(
            value=rarity in saved_rarities
        )
        for rarity in RARITIES
    }

    filter_visible = False

    filter_on_image = tk.PhotoImage(
        file=os.path.join(UI_DIR, "filter_on.png")
    )

    filter_off_image = tk.PhotoImage(
        file=os.path.join(UI_DIR, "filter_off.png")
    )

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
        image=filter_off_image,
        command=toggle_filters,
        bg=style.BUTTON_NORMAL,
        activebackground=style.BUTTON_CLICKED,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2",
        padx=0,
        pady=0
    )

    filter_button.filter_on_image = filter_on_image
    filter_button.filter_off_image = filter_off_image

    filter_button.pack(
        side="left",
        padx=(6, 0)
    )

    def update_filter_icon():

        selected_rarities = [
            rarity
            for rarity, variable in rarity_vars.items()
            if variable.get()
        ]

        filters_active = (
            sort_var.get() != "Rarity"
            or len(selected_rarities) != len(RARITIES)
        )

        if filters_active:
            filter_button.config(
                image=filter_button.filter_on_image
            )
        else:
            filter_button.config(
                image=filter_button.filter_off_image
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

        selected_rarities = [
            rarity
            for rarity, variable in rarity_vars.items()
            if variable.get()
        ]

        if len(selected_rarities) == len(RARITIES):
            rarity_text = "All rarities"

        elif not selected_rarities:
            rarity_text = "No rarities selected"

        else:
            rarity_text = ", ".join(selected_rarities)

        summary.config(
            text=f"{rarity_text} • {sort_text}"
        )

    def apply_change():

        # Save the current filter preferences
        config.setdefault("settings", {})[filter_key] = {
            "sort": sort_var.get(),
            "rarities": [
                rarity
                for rarity, variable in rarity_vars.items()
                if variable.get()
            ]
        }

        save_config(config)

        update_summary()
        update_filter_icon()
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

    # Multiple rarity checkboxes
    rarity_wrapper = tk.Frame(
        controls,
        bg="#FFE8AD"
    )

    rarity_wrapper.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3
    )

    tk.Label(
        rarity_wrapper,
        text="RARITY",
        font=style.SMALL_FONT,
        bg="#FFE8AD",
        fg=style.MUTED_TEXT
    ).pack(
        anchor="w",
        pady=(0, 3)
    )

    rarity_dropdown = tk.Button(
        rarity_wrapper,
        text="All rarities",
        font=style.TEXT_FONT,
        bg=style.BUTTON_NORMAL,
        fg=style.TEXT_COLOR,
        activebackground=style.BUTTON_CLICKED,
        activeforeground=style.TEXT_COLOR,
        relief="raised",
        bd=1,
        cursor="hand2",
        anchor="w",
        padx=6,
        pady=3
    )

    rarity_dropdown.pack(fill="x")

    # Dropdown popup
    main_window = parent.winfo_toplevel()

    rarity_popup = tk.Toplevel(main_window)
    rarity_popup.withdraw()
    rarity_popup.overrideredirect(True)

    rarity_popup.transient(main_window)

    rarity_popup.configure(
        bg="#FFE8AD"
    )

    rarity_popup_frame = tk.Frame(
        rarity_popup,
        bg="#FFE8AD",
        highlightbackground=style.BORDER_COLOR,
        highlightthickness=1
    )

    rarity_popup_frame.pack(fill="both", expand=True)

    # Colour of the selected checkmark
    CHECKMARK_COLOR = "#89604F"

    def update_rarity_dropdown():

        selected = [
            rarity
            for rarity, variable in rarity_vars.items()
            if variable.get()
        ]

        if len(selected) == len(RARITIES):
            label = "All rarities"

        elif not selected:
            label = "No rarities selected"

        else:
            label = f"Rarity ({len(selected)} selected)"

        rarity_dropdown.config(text=label)

        # Update the checkmarks
        for rarity, checkmark in rarity_checkmarks.items():

            if rarity_vars[rarity].get():
                checkmark.config(
                    text="✓",
                    fg=CHECKMARK_COLOR
                )
            else:
                checkmark.config(
                    text="",
                    fg=CHECKMARK_COLOR
                )

    def toggle_rarity(rarity):

        # Toggle the selected rarity
        rarity_vars[rarity].set(
            not rarity_vars[rarity].get()
        )

        # Refresh dropdown text and checkmarks
        update_rarity_dropdown()

        # Save preferences and refresh inventory
        apply_change()


    def toggle_rarity_popup():

        try:
            if not rarity_popup.winfo_exists():
                return

            if rarity_popup.winfo_viewable():
                rarity_popup.withdraw()
                return

            x = rarity_dropdown.winfo_rootx()
            y = (
                rarity_dropdown.winfo_rooty()
                + rarity_dropdown.winfo_height()
            )

            rarity_popup.geometry(f"+{x}+{y}")
            rarity_popup.deiconify()
            rarity_popup.lift(main_window)
            rarity_popup.lift()
            rarity_popup.focus_force()

        except tk.TclError:
            return

    rarity_checkmarks = {}

    for rarity in RARITIES:

        rarity_row = tk.Frame(
            rarity_popup_frame,
            bg="#FFE8AD",
            cursor="hand2"
        )

        rarity_row.pack(
            fill="x",
            padx=5,
            pady=2
        )

        rarity_label = tk.Label(
            rarity_row,
            text=rarity,
            font=style.TEXT_FONT,
            bg="#FFE8AD",
            fg=style.TEXT_COLOR,
            anchor="w",
            width=15
        )

        rarity_label.pack(
            side="left",
            padx=5,
            pady=4
        )

        checkmark = tk.Label(
            rarity_row,
            text="",
            font=("Arial", 12, "bold"),
            bg="#FFE8AD",
            fg=CHECKMARK_COLOR,
            width=3
        )

        checkmark.pack(
            side="right",
            padx=5
        )

        rarity_checkmarks[rarity] = checkmark

        # Make the entire row clickable
        for widget in (
            rarity_row,
            rarity_label,
            checkmark
        ):
            widget.bind(
                "<Button-1>",
                lambda event, r=rarity: toggle_rarity(r)
            )

    rarity_dropdown.config(
        command=toggle_rarity_popup
    )

    def close_rarity_popup(event):
        try:
            if not rarity_popup.winfo_exists():
                return

            if not rarity_popup.winfo_viewable():
                return

            widget = event.widget

            if widget == rarity_dropdown:
                return

            if widget.winfo_toplevel() == rarity_popup:
                return

            rarity_popup.withdraw()

        except tk.TclError:
            return

    # Register the global click handler once.
    close_binding_id = parent.bind_all(
        "<Button-1>",
        close_rarity_popup,
        add="+"
    )

    def cleanup_rarity_popup(event):
        if event.widget != parent:
            return

        # Remove only this popup's global click handler.
        try:
            if close_binding_id:
                parent._unbind(
                    ("bind", "all", "<Button-1>"),
                    close_binding_id
                )
        except tk.TclError:
            pass

        # Destroy the popup when its tab is destroyed.
        try:
            if rarity_popup.winfo_exists():
                rarity_popup.destroy()
        except tk.TclError:
            pass

    parent.bind(
        "<Destroy>",
        cleanup_rarity_popup,
        add="+"
    )

    update_rarity_dropdown()
    update_filter_icon()

    # Reset button
    def reset_filters():

        sort_var.set("Rarity")

        # Select every rarity
        for variable in rarity_vars.values():
            variable.set(True)

        # Refresh the dropdown and checkmarks
        update_rarity_dropdown()

        # Save and refresh inventory
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

    return sort_var, rarity_vars

def get_filtered_inventory(hat_manager, sort_mode, rarity_filter):

    owned = list(hat_manager.owned)

    # Sorting
    if sort_mode == "Rarity":
        owned = hat_manager.get_sorted_inventory()

    elif sort_mode == "Newest":
        owned.reverse()

    elif sort_mode == "Oldest":
        pass

    elif sort_mode == "A-Z":
        owned.sort(
            key=lambda item:
                hat_manager.catalog[item["hat_id"]]["name"].casefold()
        )

    elif sort_mode == "Z-A":
        owned.sort(
            key=lambda item:
                hat_manager.catalog[item["hat_id"]]["name"].casefold(),
            reverse=True
        )

    if isinstance(rarity_filter, dict):

        selected_rarities = {
            rarity
            for rarity, variable in rarity_filter.items()
            if variable.get()
        }

    elif isinstance(rarity_filter, str):

        selected_rarities = (
            set(RARITIES)
            if rarity_filter == "All rarities"
            else {rarity_filter}
        )

    else:

        selected_rarities = set(rarity_filter or [])

    # Empty selection means show everything
    if not selected_rarities:
        owned = []

    else:
        owned = [
            item
            for item in owned
            if hat_manager.catalog[
                item["hat_id"]
            ]["rarity"] in selected_rarities
        ]

    return owned
