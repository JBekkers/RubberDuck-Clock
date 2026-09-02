from Source.Config.style import CENTER_X, CENTER_Y
from Source.Window_Manager import root, canvas, start_move, move_window
from Source.Config.paths import SPRITES_DIR, DATA_DIR

from dataclasses import dataclass

import random
import json
import os

from PIL import Image, ImageTk
from Source.sound import play_sound
import time

from Source.Config.effects import EffectManager


SPRITE_SIZE = (150, 150)

ANIMATION_FILE = os.path.join(DATA_DIR, "animations.json")

@dataclass
class Animation:
    frames: list[Image.Image]
    speed: int
    looping: bool
    loop_time: float | int | list[float]
    next_animation: str
    weight: float
    isRare: bool = False
    sound: str | None = None
    effect: str | None = None
    current_loop_time: float = 0

animations: dict[str, Animation] = {}
current_animation = "Idle"
current_frame = 0
loop_start_time = None
app_config = None

effect_manager = None

def get_current_animation():
    return current_animation

def start_effect(effect_name):

    if effect_manager is None:
        return False

    return effect_manager.start(effect_name)

def set_config(config):
    global app_config
    app_config = config


def record_rare_animation(name):
    if app_config is None:
        return

    animation = animations.get(name)

    if animation is None or not animation.isRare:
        return

    app_config["rare_animations_seen"] = (
        app_config.get("rare_animations_seen", 0) + 1
    )

    discovered = app_config.get(
        "rare_animations_discovered",
        []
    )

    if name not in discovered:
        discovered.append(name)
        app_config["rare_animations_discovered"] = discovered

    from Source.Config.config import save_config
    save_config(app_config)

def load_animation(
    name,
    frame_width,
    frame_height,
    speed,
    looping=False,
    loop_time=0,
    next_animation="Idle",
    weight=0,
    sound=None,
    isRare=False,
    effect=None,
):

    sheet = Image.open(
        os.path.join(SPRITES_DIR, f"{name}.png")
    ).convert("RGBA")

    frames = []

    for i in range(sheet.height // frame_height):

        frame = sheet.crop((
            0,
            i * frame_height,
            frame_width,
            (i + 1) * frame_height
        ))

        frame = frame.resize(
            SPRITE_SIZE,
            Image.Resampling.NEAREST
        )

        frames.append(frame)


    animations[name] = Animation(
        frames=frames,
        speed=speed,
        looping=looping,
        loop_time=loop_time,
        next_animation=next_animation,
        weight=weight,
        sound=sound,
        isRare=isRare,
        effect=effect,
    )

with open(ANIMATION_FILE, "r") as f:
    animation_data = json.load(f)

default = animation_data["default"]


for name, data in animation_data["animations"].items():

    load_animation(
        name=name,
        frame_width=default["frame_width"],
        frame_height=default["frame_height"],
        speed=data["speed"],
        looping=data.get("looping", False),
        loop_time=data.get("loop_time", 0),
        next_animation=data.get("next", "Idle"),
        weight=data.get("weight", 0),
        sound=data.get("sound"),
        isRare=data.get("isRare", False),
        effect=data.get("effect"),
    )

initial_frame = animations[current_animation].frames[0]

initial_photo = ImageTk.PhotoImage(initial_frame)

sprite_id = canvas.create_image(
    CENTER_X,
    CENTER_Y,
    image=initial_photo,
    anchor="center",
    tags=("draggable",)
)

canvas.image = initial_photo

def animate_sprite():

    global current_animation
    global current_frame

    # --------------------------------------------------------
    # Update effects
    # --------------------------------------------------------

    if effect_manager is not None:
        effect_manager.update()

    # --------------------------------------------------------
    # Position duck
    # --------------------------------------------------------

    scale = (
        effect_manager.scale
        if effect_manager is not None
        else 1.0
    )

    x = canvas.winfo_width() // 2

    y = (
        canvas.winfo_height()
        - (SPRITE_SIZE[1] * scale) / 2
    )

    canvas.coords(
        sprite_id,
        x,
        y
    )

    # --------------------------------------------------------
    # Current animation
    # --------------------------------------------------------

    animation = animations[current_animation]

    frames = animation.frames

    if not frames:

        root.after(
            animation.speed,
            animate_sprite
        )

        return

    # Safety check.
    if current_frame >= len(frames):
        current_frame = 0

    frame = frames[current_frame]

    # --------------------------------------------------------
    # Scale frame
    # --------------------------------------------------------

    width = max(
        1,
        int(frame.width * scale)
    )

    height = max(
        1,
        int(frame.height * scale)
    )

    if scale == 1.0:

        resized_frame = frame

    else:

        resized_frame = frame.resize(
            (width, height),
            Image.Resampling.NEAREST
        )

    # --------------------------------------------------------
    # Convert to Tkinter image
    # --------------------------------------------------------

    photo = ImageTk.PhotoImage(
        resized_frame
    )

    canvas.itemconfig(
        sprite_id,
        image=photo
    )

    # Keep reference alive.
    canvas.image = photo

    # --------------------------------------------------------
    # Advance frame
    # --------------------------------------------------------

    current_frame += 1

    # --------------------------------------------------------
    # Animation finished
    # --------------------------------------------------------

    if current_frame >= len(frames):

        if animation.looping:

            elapsed = (
                time.monotonic() - loop_start_time
                if loop_start_time is not None
                else 0
            )

            if elapsed >= animation.current_loop_time:

                finish_current_animation(
                    animation
                )

            else:

                current_frame = 0

        else:

            finish_current_animation(
                animation
            )

    # --------------------------------------------------------
    # Next frame
    # --------------------------------------------------------

    root.after(
        animation.speed,
        animate_sprite
    )

def choose_random_animation():

    if current_animation != "Idle":

        root.after(
            2000,
            choose_random_animation
        )

        return

    choices = []
    weights = []

    for name, anim in animations.items():

        if anim.weight > 0:

            choices.append(name)
            weights.append(anim.weight)

    if choices:

        animation_name = random.choices(
            choices,
            weights=weights,
            k=1
        )[0]

        play_animation(
            animation_name
        )

    root.after(
        random.randint(3000, 10000),
        choose_random_animation
    )

def play_animation(name):

    global current_animation
    global current_frame
    global loop_start_time

    if name not in animations:

        print(
            f"Warning: animation '{name}' does not exist."
        )

        return

    current_animation = name
    current_frame = 0

    record_rare_animation(name)

    loop_start_time = time.monotonic()

    animation = animations[current_animation]

    if animation.looping:

        loop_time = animation.loop_time

        if isinstance(loop_time, list):

            animation.current_loop_time = random.uniform(
                loop_time[0],
                loop_time[1]
            )

        else:

            animation.current_loop_time = loop_time

    if animation.sound:

        play_sound(
            animation.sound
        )

effect_manager = EffectManager(
    root=root,
    get_current_animation=get_current_animation,
    play_animation=play_animation,
)

def finish_current_animation(animation):

    # --------------------------------------------------------
    # Special effect
    # --------------------------------------------------------

    if animation.effect:

        handled = start_effect(
            animation.effect
        )

        if handled:

            play_animation("Idle")

            return

    # --------------------------------------------------------
    # Normal animation
    # --------------------------------------------------------

    play_animation(
        animation.next_animation
    )

def duck_clicked(event):

    if current_animation.startswith("Sleeping"):
        play_animation("Mad_Start")
        return

def is_idle():
    return current_animation == "Idle"
