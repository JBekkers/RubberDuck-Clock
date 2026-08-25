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

SPRITE_SIZE = (150, 150)

ANIMATION_FILE = os.path.join(DATA_DIR, "animations.json")

@dataclass
class Animation:
    frames:list[ImageTk.PhotoImage]
    speed:int
    looping:bool
    loop_time:float |int | list[float]
    next_animation:str
    weight:float
    sound: str | None = None 
    current_loop_time: float = 0

animations: dict[str, Animation] = {}
current_animation = "Idle"
current_frame = 0
loop_start_time = None
app_config = None

# Animations that count as rare discoveries.
RARE_ANIMATIONS = {"RBGmode"}


def set_config(config):
    global app_config
    app_config = config


def record_rare_animation(name):
    if name not in RARE_ANIMATIONS or app_config is None:
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

        frames.append(ImageTk.PhotoImage(frame))


    animations[name] = Animation(
        frames=frames,
        speed=speed,
        looping=looping,
        loop_time=loop_time,
        next_animation=next_animation,
        weight=weight,
        sound=sound,
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
        sound=data.get("sound")
    )

sprite_id = canvas.create_image(
    CENTER_X,
    CENTER_Y,
    image=animations[current_animation].frames[0],
    anchor="center",
    tags=("draggable",)
)

def animate_sprite():

    canvas.coords(
        sprite_id,
        canvas.winfo_width() // 2,
        canvas.winfo_height() - SPRITE_SIZE[1] // 2
    )

    global current_animation
    global current_frame

    animation = animations[current_animation]
    frames = animation.frames

    canvas.itemconfig(
        sprite_id,
        image=frames[current_frame]
    )

    current_frame += 1

    if current_frame == len(frames):

        if animation.looping:

            elapsed = (
                time.monotonic() - loop_start_time
                if loop_start_time is not None
                else 0
            )   

            if elapsed >= animation.current_loop_time:
                play_animation(animation.next_animation)
            else:
                current_frame = 0

        else:

            play_animation(animation.next_animation)

    root.after(
        animation.speed,
        animate_sprite
    )

def choose_random_animation():
    if current_animation != "Idle":
        root.after(2000, choose_random_animation)
        return

    choices = []
    weights = []

    for name, anim in animations.items():
        if anim.weight > 0:
            choices.append(name)
            weights.append(anim.weight)

    if choices:
        animation = random.choices(
            choices,
            weights=weights,
            k=1
        )[0]

        play_animation(animation)

    root.after(random.randint(3000, 10000), choose_random_animation)

def play_animation(name):
    global current_animation
    global current_frame
    global loop_start_time

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
        play_sound(animation.sound)

def duck_clicked(event):

    if current_animation.startswith("Sleeping"):
        play_animation("Mad_Start")
        return

def is_idle():
    return current_animation == "Idle"
