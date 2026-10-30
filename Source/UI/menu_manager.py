import pystray
from Source.Window_Manager import root, canvas, set_always_on_top
from Source.Config.paths import ASSETS_DIR, UI_DIR

from PIL import Image, ImageTk
from Source.hats import RARITIES

import os
import threading

from Source.clock import timezone_changed

from Source.UI.app import reset_position, shutdown, restart_application
from Source.UI.Menu_Tabs.tab_loader import open_settings

from Source.UI.Menu_Button import (
    create_menu_button,
    set_reward_claim_callback,
    set_reward_available,
)

hat_manager = None
reward_timer_running = False

reward_popup_items = []
reward_popup_images = []

reward_popup_hide_job = None
reward_popup_visible = False

settings = None
config = None
particle_system = None
stats = None

def create_speech_bubble(image, size):
    image = image.convert("RGBA")

    target_width, target_height = size

    source_width, source_height = image.size

    # Fixed corner dimensions from the original bubble.
    left = 22
    right = 18
    top = 16
    bottom = 22

    source_x = [
        0,
        left,
        source_width - right,
        source_width
    ]

    source_y = [
        0,
        top,
        source_height - bottom,
        source_height
    ]

    target_x = [
        0,
        left,
        target_width - right,
        target_width
    ]

    target_y = [
        0,
        top,
        target_height - bottom,
        target_height
    ]

    result = Image.new(
        "RGBA",
        size,
        (0, 0, 0, 0)
    )

    for row in range(3):
        for column in range(3):

            patch = image.crop((
                source_x[column],
                source_y[row],
                source_x[column + 1],
                source_y[row + 1]
            ))

            patch_width = (
                target_x[column + 1]
                - target_x[column]
            )

            patch_height = (
                target_y[row + 1]
                - target_y[row]
            )

            if patch.size != (
                patch_width,
                patch_height
            ):
                patch = patch.resize(
                    (patch_width, patch_height),
                    Image.Resampling.NEAREST
                )

            result.alpha_composite(
                patch,
                (
                    target_x[column],
                    target_y[row]
                )
            )

    return result

def show_hat_reward(hat):

    global reward_popup_items
    global reward_popup_images
    global reward_popup_hide_job
    global reward_popup_visible

    # Cancel an existing notification timer.
    if reward_popup_hide_job is not None:
        root.after_cancel(reward_popup_hide_job)
        reward_popup_hide_job = None

    # Hide an existing notification.
    if reward_popup_items:
        for item in reward_popup_items:
            canvas.itemconfig(item, state="hidden")

    reward_popup_images.clear()

    bubble_path = os.path.join(
        UI_DIR,
        "Speech_Bubble.png"
    )

    bubble = Image.open(
        bubble_path
    ).convert("RGBA")

    bubble = create_speech_bubble(
        bubble,
        (170, 70)
    )

    bubble_photo = ImageTk.PhotoImage(
        bubble,
        master=root
    )

    reward_popup_images.append(bubble_photo)

    hat_image = Image.open(
        hat["path"]
    ).convert("RGBA")

    hat_image.thumbnail(
        (34,34),
        Image.Resampling.NEAREST
    )

    hat_photo = ImageTk.PhotoImage(
        hat_image,
        master=root
    )

    reward_popup_images.append(hat_photo)

    ## was 150
    bubble_x = 465
    bubble_y = 70

    bubble_item = canvas.create_image(
        bubble_x,
        bubble_y,
        image=bubble_photo,
        anchor="center",
        tags=("hat_reward_popup",)
    )

    hat_item = canvas.create_image(
        415,
        65,
        image=hat_photo,
        anchor="center",
        tags=("hat_reward_popup",)
    )

    heading_item = canvas.create_text(
        441,
        45,
        text="You got a new hat!",
        anchor="nw",
        fill="#222222",
        font=("Pxls SemiBold", 8),
        tags=("hat_reward_popup",)
    )

    name_item = canvas.create_text(
        441,
        66,
        text=hat["name"],
        anchor="nw",
        fill="#222222",
        font=("Pxls SemiBold", 8),
        width=112,
        tags=("hat_reward_popup",)
    )

    rarity_color = RARITIES[hat["rarity"]]["color"]

    rarity_item = canvas.create_text(
        441,
        80,
        text=hat["rarity"],
        anchor="nw",
        fill=rarity_color,
        font=("Pxls SemiBold", 6),
        tags=("hat_reward_popup",)
    )

    reward_popup_items = [
        bubble_item,
        hat_item,
        heading_item,
        name_item,
        rarity_item
    ]

    # Make sure the entire notification appears above the duck.
    canvas.tag_raise("hat_reward_popup")

    reward_popup_visible = True

    def hide_reward_popup():
        global reward_popup_hide_job
        global reward_popup_visible

        for item in reward_popup_items:
            canvas.itemconfig(
                item,
                state="hidden"
            )

        reward_popup_hide_job = None
        reward_popup_visible = False

    reward_popup_hide_job = root.after(
        5000,
        hide_reward_popup
    )

def check_hat_reward():
    if hat_manager is None:
        return

    available = hat_manager.is_drop_available()

    set_reward_available(available)

    root.after(
        1000,
        check_hat_reward
    )


def claim_hat_reward():
    if hat_manager is None:
        return

    hat = hat_manager.claim_drop()

    if hat is None:
        return

    set_reward_available(False)

    from Source.animation import play_animation

    show_hat_reward(hat)

    play_animation("Happy_Quack")

def setup_menu(
    app_settings,
    app_config,
    app_stats,
    app_particle_system,
    app_hat_manager
):
    global settings, config, stats, particle_system, hat_manager

    settings = app_settings
    config = app_config
    stats = app_stats
    particle_system = app_particle_system
    hat_manager = app_hat_manager

    set_reward_claim_callback(
        claim_hat_reward
    )

    root.after(
        1000,
        check_hat_reward
    )

    create_tray_icon()

    threading.Thread(
        target=icon.run,
        daemon=True
    ).start()


def tray_reset_position(icon, item):
    reset_position(config)

def tray_restart_app(icon, item):
    restart_application(config, stats, icon)

def tray_quit_app(icon, item):
    root.after(
        0,
        lambda: shutdown(config, stats, icon)
    )

tray_icon = Image.open(os.path.join(ASSETS_DIR, "Icon.png"))

icon = None


def create_tray_icon():

    global icon

    icon = pystray.Icon(
        "Duck Clock",
        tray_icon,
        "Duck Clock",
        menu=pystray.Menu(

            pystray.MenuItem(
                "Reset Clock Position",
                tray_reset_position
            ),


            pystray.MenuItem(
                "Restart Application",
                tray_restart_app
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Quit Application",
                tray_quit_app
            ),
        ),
    )

def toggle_menu(event=None):

    actions = {
        "reset_position": lambda: reset_position(config),
        "quit": lambda: shutdown(config, stats, icon),
        "restart": lambda: restart_application(config, stats, icon),

        "disable_particles": lambda disabled:
            particle_system.set_disabled(
                "Bubbles",
                disabled
            ),

        "always_on_top": set_always_on_top,
        "sound_volume": 100,

        "timezone_changed": timezone_changed
    }

    open_settings(
        root,
        settings,
        config,
        stats,
        actions,
        hat_manager
    )
    
create_menu_button(toggle_menu)