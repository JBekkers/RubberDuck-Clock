from PIL import Image, ImageTk
import os

from Source.Window_Manager import canvas
from Source.Config.paths import UI_DIR
from Source.Config import style

menu_image = None
menu_hover = None
menu_button = None

reward_icon_image = None
reward_indicator = None
reward_claim_callback = None
reward_available = False

def set_reward_claim_callback(callback):
    global reward_claim_callback
    reward_claim_callback = callback


def set_reward_available(available):
    global reward_available

    reward_available = available

    if reward_indicator is None:
        return

    canvas.itemconfig(
        reward_indicator,
        state="normal" if available else "hidden"
    )

def create_menu_button(open_menu):

    global menu_button
    global menu_image
    global menu_hover
    global reward_icon_image
    global reward_indicator

    # Load menu images
    menu_image = ImageTk.PhotoImage(
        Image.open(
            os.path.join(UI_DIR, "MenuIcon.png")
        ).convert("RGBA")
    )

    menu_hover = ImageTk.PhotoImage(
        Image.open(
            os.path.join(UI_DIR, "MenuIconHover.png")
        ).convert("RGBA")
    )

    # Create main menu button
    menu_button = canvas.create_image(
        75 + style.MENU_OFFSET_X,
        75 + style.MENU_OFFSET_Y,
        image=menu_image,
        anchor="center",
        tags=("menu_button",),
    )

    canvas.tag_bind(
        "menu_button",
        "<Button-1>",
        open_menu
    )

    canvas.tag_bind(
        "menu_button",
        "<Enter>",
        lambda e: (
            canvas.itemconfig(menu_button, image=menu_hover),
            canvas.config(cursor="hand2")
        )
    )

    canvas.tag_bind(
        "menu_button",
        "<Leave>",
        lambda e: (
            canvas.itemconfig(menu_button, image=menu_image),
            canvas.config(cursor="")
        )
    )

    hatdrop_pil = Image.open(os.path.join(UI_DIR, "NewHatIcon.png")).convert("RGBA")
    
    # Resize while preserving aspect ratio
    hatdrop_pil.thumbnail((26, 26),Image.Resampling.NEAREST)

    reward_icon_image = ImageTk.PhotoImage(hatdrop_pil)

    # Create clickable hat drop icon
    reward_indicator = canvas.create_image(
        75 + style.MENU_OFFSET_X + 25,
        75 + style.MENU_OFFSET_Y - 20,
        image=reward_icon_image,
        anchor="center",
        tags=("hat_reward",),
        state="hidden"
    )

    canvas.tag_bind(
        "hat_reward",
        "<Button-1>",
        lambda event: (
            reward_claim_callback()
            if reward_claim_callback is not None
            else None
        )
    )

    canvas.tag_bind(
        "hat_reward",
        "<Enter>",
        lambda event: canvas.config(cursor="hand2")
    )

    canvas.tag_bind(
        "hat_reward",
        "<Leave>",
        lambda event: canvas.config(cursor="")
    )

    canvas.tag_raise(reward_indicator)

    