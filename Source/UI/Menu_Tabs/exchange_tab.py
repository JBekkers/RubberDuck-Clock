
import random
import tkinter as tk
from PIL import Image, ImageTk

from Source.Config import style
from Source.Config.scrollbar import FlatScrollbar, enable_mousewheel
from Source.hats import RARITIES, RARITY_ORDER

UPGRADE_ORDER = list(reversed(RARITY_ORDER))

SLOT_COUNT = 10


def build_exchange_tab(parent, settings, config, hat_manager):
    for widget in parent.winfo_children():
        widget.destroy()

    selected_instances = []
    selected_rarity = None
    slot_buttons = []
    inventory_cards = {}
    photo_references = []

    header = tk.Label(
        parent,
        text="Exchange",
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    )
    header.pack(pady=(0, 6))

    slots_frame = tk.Frame(
        parent,
        bg=style.BACKGROUND
    )
    slots_frame.pack(fill="x", pady=(0, 6))

    for column in range(5):
        slots_frame.columnconfigure(column, weight=1, uniform="slot")

    def remove_from_slot(instance_id):
        if instance_id in selected_instances:
            selected_instances.remove(instance_id)
            update_exchange_view()

    for slot_index in range(SLOT_COUNT):
        border = tk.Frame(
            slots_frame,
            bg=style.DISABLED_BACKGROUND,
            padx=3,
            pady=3
        )

        border.grid(
            row=slot_index // 5,
            column=slot_index % 5,
            padx=3,
            pady=3,
            sticky="nsew"
        )

        button = tk.Button(
            border,
            text="Empty",
            font=style.SMALL_FONT,
            bg=style.DISABLED_BACKGROUND,
            fg=style.TEXT_COLOR,
            activebackground=style.BUTTON_CLICKED,
            relief="flat",
            width=10,
            height=5,
            state="disabled",
            cursor="arrow"
        )
        button.pack(fill="both", expand=True)
        border.config(width=64, height=64)
        border.pack_propagate(False)

        slot_buttons.append((border, button))

    status_label = tk.Label(
        parent,
        text="Select 10 Common hats to begin.",
        font=style.SMALL_FONT,
        bg=style.BACKGROUND,
        fg=style.MUTED_TEXT
    )
    status_label.pack(pady=(0, 5))

    exchange_button = tk.Button(
        parent,
        text="Exchange",
        font=style.BUTTON_FONT,
        bg=style.DISABLED_BACKGROUND,
        fg=style.MUTED_TEXT,
        activebackground=style.BUTTON_CLICKED,
        relief="flat",
        state="disabled",
        cursor="arrow",
        command=lambda: perform_exchange()
    )
    exchange_button.pack(fill="x", pady=(0, 8))

    inventory_heading = tk.Label(
        parent,
        text="Inventory",
        font=style.TEXT_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    )
    inventory_heading.pack(anchor="w", pady=(0, 3))

    inventory_container = tk.Frame(
        parent,
        bg=style.BACKGROUND
    )
    inventory_container.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        inventory_container,
        bg=style.BACKGROUND,
        highlightthickness=0
    )
    enable_mousewheel(canvas)

    scrollbar = FlatScrollbar(
        inventory_container,
        command=canvas.yview,
        bg=style.SCROLLBAR_BACKGROUND,
        width=style.SCROLLBAR_WIDTH,
        thumb_color=style.SCROLLBAR_THUMB,
        hover_color=style.SCROLLBAR_THUMB_HOVER,
        thumb_width=style.SCROLLBAR_THUMB_WIDTH,
        thumb_height=style.SCROLLBAR_THUMB_HEIGHT,
        arrow_height=style.SCROLLBAR_ARROW_HEIGHT,
        arrow_color=style.SCROLLBAR_ARROW_COLOR,
        arrow_hover_color=style.SCROLLBAR_ARROW_HOVER
    )

    scrollbar.pack(side="right", fill="y")

    grid = tk.Frame(
        canvas,
        bg=style.BACKGROUND
    )

    grid_window = canvas.create_window(
        (0, 0),
        window=grid,
        anchor="nw"
    )

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)

    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def update_grid_width(event):
        canvas.itemconfigure(
            grid_window,
            width=event.width
        )

    grid.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", update_grid_width)

    def select_hat(instance_id):
        nonlocal selected_rarity

        # Do not allow the same inventory occurrence twice.
        if instance_id in selected_instances:
            remove_from_slot(instance_id)
            return

        owned_item = next(
            (
                item for item in hat_manager.owned
                if item["instance_id"] == instance_id
            ),
            None
        )

        if owned_item is None:
            return

        hat = hat_manager.catalog[owned_item["hat_id"]]
        rarity = hat["rarity"]

        # Legendary hats cannot be exchanged for now.
        if rarity == "Legendary":
            status_label.config(
                text="Legendary hats cannot be exchanged.",
                fg=RARITIES["Legendary"]["color"]
            )
            return

        # The first selection determines the allowed rarity.
        if selected_rarity is None:
            selected_rarity = rarity

        if rarity != selected_rarity:
            status_label.config(
                text=f"Select only {selected_rarity} hats.",
                fg=style.TEXT_COLOR
            )
            return

        if len(selected_instances) >= SLOT_COUNT:
            return

        selected_instances.append(instance_id)
        update_exchange_view()

    def update_exchange_view():
        nonlocal selected_rarity

        # Keep only selections that still exist in the inventory.
        owned_ids = {
            item["instance_id"]
            for item in hat_manager.owned
        }

        selected_instances[:] = [
            instance_id
            for instance_id in selected_instances
            if instance_id in owned_ids
        ]

        if not selected_instances:
            selected_rarity = None
        else:
            first_item = next(
                item for item in hat_manager.owned
                if item["instance_id"] == selected_instances[0]
            )
            selected_rarity = hat_manager.catalog[
                first_item["hat_id"]
            ]["rarity"]

        # Update the 10 slots.
        for slot_index, (border, button) in enumerate(slot_buttons):
            if slot_index < len(selected_instances):
                instance_id = selected_instances[slot_index]

                item = next(
                    item for item in hat_manager.owned
                    if item["instance_id"] == instance_id
                )
                hat = hat_manager.catalog[item["hat_id"]]

                try:
                    image = Image.open(hat["path"]).convert("RGBA")
                    image.thumbnail((50, 50), Image.Resampling.NEAREST)

                    photo = ImageTk.PhotoImage(image, master=button)
                    button.image = photo

                    button.config(
                        image=photo,
                        bg=style.BUTTON_NORMAL,
                        fg=style.TEXT_COLOR,
                        state="normal",
                        cursor="hand2",
                        command=lambda selected_id=instance_id:
                            remove_from_slot(selected_id)
                    )
                    button.image = photo

                except (OSError, ValueError):
                    button.config(
                        image="",
                        bg=style.BUTTON_NORMAL,
                        fg=style.TEXT_COLOR,
                        state="normal",
                        cursor="hand2",
                        command=lambda selected_id=instance_id:
                            remove_from_slot(selected_id)
                    )
                    button.image = None

                border.config(bg=RARITIES[hat["rarity"]]["color"])

            else:
                border.config(bg=style.DISABLED_BACKGROUND)

                button.config(
                    text="Empty",
                    image="",
                    bg=style.DISABLED_BACKGROUND,
                    fg=style.DISABLED_BACKGROUND,
                    state="disabled",
                    cursor="arrow",
                    command=lambda: None
                )
                button.image = None

        # Enable Exchange only when all 10 slots are filled.
        ready = len(selected_instances) == SLOT_COUNT

        exchange_button.config(
            state="normal" if ready else "disabled",
            bg=style.BUTTON_NORMAL if ready else style.DISABLED_BACKGROUND,
            fg=style.TEXT_COLOR if ready else style.MUTED_TEXT,
            cursor="hand2" if ready else "arrow"
        )

        if ready:
            target_rarity = UPGRADE_ORDER[
                UPGRADE_ORDER.index(selected_rarity) + 1
            ]
            status_label.config(
                text=f"10 {selected_rarity} hats → 1 random {target_rarity}",
                fg=style.TEXT_COLOR
            )
        elif selected_rarity is not None:
            status_label.config(
                text=f"Selected {len(selected_instances)}/10 {selected_rarity} hats",
                fg=style.TEXT_COLOR
            )
        else:
            status_label.config(
                text="Select 10 hats of the same rarity. Legendary hats are excluded.",
                fg=style.MUTED_TEXT
            )

        # Update the inventory cards to show selected and locked hats.
        for instance_id, widgets in inventory_cards.items():
            item = next(
                (
                    item for item in hat_manager.owned
                    if item["instance_id"] == instance_id
                ),
                None
            )

            if item is None:
                continue

            hat = hat_manager.catalog[item["hat_id"]]
            rarity = hat["rarity"]

            selected = instance_id in selected_instances
            locked = (
                rarity == "Legendary"
                or (
                    selected_rarity is not None
                    and rarity != selected_rarity
                )
                or len(selected_instances) >= SLOT_COUNT
            )

            background = (
                "#FCE9AD" if selected
                else style.DISABLED_BACKGROUND if locked
                else style.BUTTON_NORMAL
            )

            foreground = (
                style.MUTED_TEXT if locked and not selected
                else style.TEXT_COLOR
            )

            for widget in widgets:
                if widget is inventory_cards[instance_id][0]:
                    widget.config(
                        bg=RARITIES[rarity]["color"],
                        cursor="arrow" if locked and not selected else "hand2"
                    )
                else:
                    widget.config(
                        bg=background,
                        cursor="arrow" if locked and not selected else "hand2"
                    )

                if isinstance(widget, tk.Label):
                    widget.config(fg=foreground)

    def perform_exchange():
        nonlocal selected_rarity

        if len(selected_instances) != SLOT_COUNT:
            return

        if selected_rarity is None or selected_rarity == "Legendary":
            return

        current_order_index = UPGRADE_ORDER.index(selected_rarity)

        if current_order_index + 1 >= len(UPGRADE_ORDER):
            return

        target_rarity = UPGRADE_ORDER[current_order_index + 1]

        rewards = [
            hat for hat in hat_manager.catalog.values()
            if hat["rarity"] == target_rarity
        ]

        if not rewards:
            status_label.config(
                text=f"No {target_rarity} hats are available in the catalog.",
                fg=style.TEXT_COLOR
            )
            return

        # Pick the reward before removing any inventory items.
        reward = random.choice(rewards)
        consumed_ids = set(selected_instances)

        # Remove exactly the selected inventory occurrences.
        hat_manager.owned[:] = [
            item for item in hat_manager.owned
            if item["instance_id"] not in consumed_ids
        ]

        # If the equipped instance was consumed, unequip it.
        if hat_manager.equipped in consumed_ids:
            hat_manager.equipped = None

        # Add the reward using the existing inventory manager.
        # add_hat() creates a new instance ID and saves the inventory.
        hat_manager.add_hat(reward["id"])

        selected_instances.clear()
        selected_rarity = None

        render_inventory()
        update_exchange_view()

        status_label.config(
            text=f"Received {reward['name']} ({target_rarity})!",
            fg=style.TEXT_COLOR
        )

    def render_inventory():
        for widget in grid.winfo_children():
            widget.destroy()

        photo_references.clear()
        inventory_cards.clear()

        owned = hat_manager.get_sorted_inventory()

        if not owned:
            tk.Label(
                grid,
                text="No hats in your inventory.",
                font=style.TEXT_FONT,
                bg=style.BACKGROUND,
                fg=style.MUTED_TEXT
            ).grid(row=0, column=0, pady=20)

            update_scroll_region()
            update_exchange_view()
            return

        columns = 5

        for column in range(columns):
            grid.columnconfigure(column, weight=1)

        for position, item in enumerate(owned):
            instance_id = item["instance_id"]
            hat = hat_manager.catalog[item["hat_id"]]
            rarity = hat["rarity"]

            row = position // columns
            column = position % columns

            border = tk.Frame(
                grid,
                bg=RARITIES[rarity]["color"],
                padx=3,
                pady=3
            )
            border.grid(
                row=row,
                column=column,
                padx=3,
                pady=3,
                sticky="nsew"
            )

            card = tk.Frame(
                border,
                bg=style.BUTTON_NORMAL,
                width=60,
                height=60
            )
            card.pack(fill="both", expand=True)
            card.pack_propagate(False)

            try:
                image = Image.open(hat["path"]).convert("RGBA")
                image.thumbnail((50, 50), Image.Resampling.NEAREST)

                photo = ImageTk.PhotoImage(image, master=grid)
                photo_references.append(photo)

                image_label = tk.Label(
                    card,
                    image=photo,
                    bg=style.BUTTON_NORMAL
                )
                image_label.image = photo
                image_label.pack(pady=(2, 0), expand=True)

            except (OSError, ValueError):
                image_label = tk.Label(
                    card,
                    text="Image unavailable",
                    font=style.SMALL_FONT,
                    bg=style.BUTTON_NORMAL,
                    fg=style.TEXT_COLOR
                )
                image_label.pack(expand=True)

            inventory_cards[instance_id] = (
                border,
                card,
                image_label,
            )

            # Bind the same selection action to the whole card.
            for widget in inventory_cards[instance_id]:
                widget.bind(
                    "<Button-1>",
                    lambda event, selected_id=instance_id:
                        select_hat(selected_id)
                )

        update_scroll_region()
        update_exchange_view()

    render_inventory()
