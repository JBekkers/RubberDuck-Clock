from PIL import Image, ImageTk
import os

from Source.Window_Manager import canvas
from Source.Config.paths import UI_DIR

MENU_OFFSET_X = 130
MENU_OFFSET_Y = 200

menu_image = None
menu_hover = None
menu_button = None


def create_menu_button(open_menu):

    global menu_button
    global menu_image
    global menu_hover

    menu_image = ImageTk.PhotoImage(
        Image.open(
            os.path.join(
                UI_DIR,
                "MenuIcon.png"
            )
        ).convert("RGBA")
    )

    menu_hover = ImageTk.PhotoImage(
        Image.open(
            os.path.join(
                UI_DIR,
                "MenuIconHover.png"
            )
        ).convert("RGBA")
    )

    menu_button = canvas.create_image(
        75 + MENU_OFFSET_X,
        75 + MENU_OFFSET_Y,
        image=menu_image,
        anchor="center",
        tags=("menu_button",)
    )

    canvas.tag_bind(
        "menu_button",
        "<Button-1>",
        open_menu
    )

    canvas.tag_bind(
        "menu_button",
        "<Enter>",
        lambda e: canvas.itemconfig(menu_button, image=menu_hover)
    )

    canvas.tag_bind(
        "menu_button",
        "<Leave>",
        lambda e: canvas.itemconfig(menu_button, image=menu_image)
    )