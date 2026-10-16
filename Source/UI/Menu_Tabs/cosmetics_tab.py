import tkinter as tk
from PIL import Image, ImageTk

from Source.Config import style
from Source.hats import RARITIES, RARITY_ORDER


def build_cosmetics_tab(
    parent,
    settings,
    config,
    hat_manager
):
    for widget in parent.winfo_children():
        widget.destroy()

    header = tk.Frame(
        parent,
        bg=style.BACKGROUND
    )
    header.pack(
        fill="x",
        pady=(0, 8)
    )

    tk.Label(
        header,
        text="Your Hats",
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(side="left")

    equipped_text = tk.Label(
        header,
        text="",
        font=style.SMALL_FONT,
        bg=style.BACKGROUND,
        fg=style.MUTED_TEXT
    )
    equipped_text.pack(side="right")

    container = tk.Frame(
        parent,
        bg=style.BACKGROUND
    )
    container.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        container,
        bg=style.BACKGROUND,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    grid = tk.Frame(
        canvas,
        bg=style.BACKGROUND
    )

    grid_window = canvas.create_window(
        (0, 0),
        window=grid,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    photo_references = []

    def update_scroll_region(event=None):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def update_grid_width(event):
        canvas.itemconfigure(
            grid_window,
            width=event.width
        )

    grid.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        update_grid_width
    )

    def render_inventory():
        for widget in grid.winfo_children():
            widget.destroy()

        photo_references.clear()

        owned = hat_manager.get_sorted_inventory()

        if not owned:
            tk.Label(
                grid,
                text="No hats yet.\nCheck back for a reward!",
                font=style.TEXT_FONT,
                bg=style.BACKGROUND,
                fg=style.MUTED_TEXT,
                justify="center"
            ).grid(
                row=0,
                column=0,
                columnspan=3,
                pady=30
            )

            equipped_text.config(
                text="No hat equipped"
            )

            update_scroll_region()
            return

        if hat_manager.equipped:
            equipped_name = hat_manager.catalog[
                hat_manager.equipped
            ]["name"]

            equipped_text.config(
                text=f"Equipped: {equipped_name}"
            )
        else:
            equipped_text.config(
                text="No hat equipped"
            )

        columns = 3

        for column in range(columns):
            grid.columnconfigure(
                column,
                weight=1
            )

        for position, (inventory_index, hat_id) in enumerate(owned):
            hat = hat_manager.catalog[hat_id]

            row = position // columns
            column = position % columns

            rarity_color = RARITIES[
                hat["rarity"]
            ]["color"]

            equipped = (
                hat_manager.equipped == hat_id
            )

            border = tk.Frame(
                grid,
                bg=rarity_color,
                padx=4,
                pady=4
            )

            border.grid(
                row=row,
                column=column,
                padx=5,
                pady=5,
                sticky="nsew"
            )

            card = tk.Frame(
                border,
                bg=style.BUTTON_NORMAL,
                width=100,
                height=100
            )

            card.pack(
                fill="both",
                expand=True
            )

            card.pack_propagate(False)

            try:
                image = Image.open(
                    hat["path"]
                ).convert("RGBA")

                image.thumbnail(
                    (64, 58),
                    Image.Resampling.NEAREST
                )

                photo = ImageTk.PhotoImage(image)

                photo_references.append(photo)

                image_label = tk.Label(
                    card,
                    image=photo,
                    bg=style.BUTTON_NORMAL
                )

                image_label.pack(
                    pady=(5, 2)
                )

            except (OSError, ValueError):
                image_label = tk.Label(
                    card,
                    text="Image\nunavailable",
                    font=style.SMALL_FONT,
                    bg=style.BUTTON_NORMAL,
                    fg=style.TEXT_COLOR
                )

                image_label.pack(
                    pady=(5, 2)
                )

            name = tk.Label(
                card,
                text=hat["name"],
                font=style.SMALL_FONT,
                bg=style.BUTTON_NORMAL,
                fg=style.TEXT_COLOR,
                wraplength=90
            )

            name.pack(
                fill="x",
                padx=2
            )

            if equipped:
                status = tk.Label(
                    card,
                    text="EQUIPPED",
                    font=style.SMALL_FONT,
                    bg=style.BUTTON_NORMAL,
                    fg=style.UNLOCKED_COLOR
                )
            else:
                status = tk.Label(
                    card,
                    text=hat["rarity"],
                    font=style.SMALL_FONT,
                    bg=style.BUTTON_NORMAL,
                    fg=style.MUTED_TEXT
                )

            status.pack(
                fill="x",
                padx=2
            )

            def select_hat(selected_id=hat_id):
                hat_manager.toggle_hat(
                    selected_id
                )
                render_inventory()

            for widget in (
                border,
                card,
                image_label,
                name,
                status
            ):
                widget.bind(
                    "<Button-1>",
                    lambda event, callback=select_hat:
                    callback()
                )

        update_scroll_region()

    render_inventory()