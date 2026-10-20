import tkinter as tk
from PIL import Image, ImageTk

from Source.Config import style
from Source.hats import RARITIES, RARITY_ORDER
from Source.Config.scrollbar import FlatScrollbar, enable_mousewheel
import time

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
        text="Inventory:",
        font=style.TITLE_FONT,
        bg=style.BACKGROUND,
        fg=style.TEXT_COLOR
    ).pack(side="left")

    droptimer_text = tk.Label(
        header,
        text="Next drop in: --",
        font=style.SMALL_FONT,
        bg=style.BACKGROUND,
        fg=style.MUTED_TEXT
    )
    droptimer_text.pack(side="right")

    
    def update_selection():
        for instance_id, widgets in inventory_cards.items():
            selected = hat_manager.equipped == instance_id

            background = (
                "#FCE9AD"
                if selected
                else style.BUTTON_NORMAL
            )

            widgets["card"].configure(bg=background)
            widgets["image_slot"].configure(bg=background)
            widgets["image_label"].configure(bg=background)
            widgets["name"].configure(bg=background)
            widgets["status"].configure(bg=background)

    def update_drop_timer():
        if not droptimer_text.winfo_exists():
            return

        remaining = max(
            0,
            int(hat_manager.next_drop_at - time.time() + 0.999)
        )

        if remaining == 0:
            droptimer_text.config(
                text="Next drop: Available!"
            )
        else:
            minutes, seconds = divmod(remaining, 60)

            droptimer_text.config(
                text=f"Next drop in: {minutes}m {seconds:02d}s"
            )

        droptimer_text.after(
            1000,
            update_drop_timer
        )

    update_drop_timer()

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

    enable_mousewheel(canvas)

    scrollbar = FlatScrollbar(
        container,
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
    inventory_cards = {}

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
        inventory_cards.clear()

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

            update_scroll_region()
            return

        columns = 3

        for column in range(columns):
            grid.columnconfigure(
                column,
                weight=1
            )
        
        for position, item in enumerate(owned):
            instance_id = item["instance_id"]
            hat_id = item["hat_id"]

            # Get the hat belonging to this inventory card.
            hat = hat_manager.catalog[hat_id]

            row = position // columns
            column = position % columns

            rarity_color = RARITIES[
                hat["rarity"]
            ]["color"]

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

            selected_background = (
                "#FCE9AD"
                if hat_manager.equipped == instance_id
                else style.BUTTON_NORMAL
            )

            card = tk.Frame(
                border,
                bg=selected_background,
                width=100,
                height=100
            )

            card.pack(
                fill="both",
                expand=True
            )

            card.pack_propagate(False)

            image_slot = tk.Frame(
                card,
                bg=selected_background,
                height=64
            )

            image_slot.pack(
                fill="x",
                padx=2,
                pady=(4, 2)
            )

            image_slot.pack_propagate(False)

            try:
                image = Image.open(
                    hat["path"]
                ).convert("RGBA")

                image.thumbnail(
                    (64, 58),
                    Image.Resampling.NEAREST
                )

                photo = ImageTk.PhotoImage(image, master=grid)
                photo_references.append(photo)

                image_label = tk.Label(
                    image_slot,
                    image=photo,
                    bg=selected_background
                )
                image_label.image = photo
                image_label.pack(expand=True)

            except (OSError, ValueError):
                image_label = tk.Label(
                    image_slot,
                    text="Image unavailable",
                    font=style.SMALL_FONT,
                    bg=selected_background,
                    fg=style.TEXT_COLOR
                )

                image_label.pack(expand=True)

            name = tk.Label(
                card,
                text=hat["name"],
                font=style.SMALL_FONT,
                bg=selected_background,
                fg=style.TEXT_COLOR,
                wraplength=90
            )

            name.pack(
                fill="x",
                padx=2
            )

            status = tk.Label(
                card,
                text=hat["rarity"],
                font=style.SMALL_FONT,
                bg=selected_background,
                fg=style.MUTED_TEXT
            )

            status.pack(
                fill="x",
                padx=2
            )

            inventory_cards[instance_id] = {
                "border": border,
                "card": card,
                "image_slot": image_slot,
                "image_label": image_label,
                "name": name,
                "status": status,
            }

            def select_hat(event, selected_instance_id=instance_id):
                hat_manager.toggle_hat(selected_instance_id)
                update_selection()

            def bind_click(widget, selected_instance_id):
                widget.bind(
                    "<Button-1>",
                    lambda event, hat_instance=selected_instance_id:
                        select_hat(event, hat_instance)
                )

            for widget in (
                border,
                card,
                image_slot,
                image_label,
                name,
                status
            ):
                bind_click(widget, instance_id)

        update_scroll_region()

    render_inventory()

