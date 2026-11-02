
import os
import tkinter.font as tkfont

from PIL import Image, ImageTk

from Source.Window_Manager import root, canvas
from Source.Config.paths import UI_DIR
from Source.hats import RARITIES
import random


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BUBBLE_PATH = os.path.join(
    UI_DIR,
    "Speech_Bubble.png"
)

FONT_FAMILY = "Pxls SemiBold"

FONT_SIZE = 8
SUBTITLE_SIZE = 8
RARITY_SIZE = 6

MAX_TEXT_WIDTH = 190

PADDING_X = 15
PADDING_Y = 12

HAT_PREVIEW_SIZE = (34, 34)

# Position relative to the canvas.
BUBBLE_X = 375
BUBBLE_Y = 70

# The dimensions of the corners that must not stretch.
NINE_SLICE = {
    "left": 22,
    "right": 18,
    "top": 16,
    "bottom": 22,
}


# --------------------------------------------------
# STATE
# --------------------------------------------------

_items = []
_images = []

_hide_job = None
_current_priority = -1
_current_animation_text = None


# --------------------------------------------------
# 9-SLICE RESIZING
# --------------------------------------------------

def resize_nine_slice(image, size):

    image = image.convert("RGBA")

    target_width, target_height = size
    source_width, source_height = image.size

    left = NINE_SLICE["left"]
    right = NINE_SLICE["right"]
    top = NINE_SLICE["top"]
    bottom = NINE_SLICE["bottom"]

    source_x = [0, left, source_width - right, source_width]
    source_y = [0, top, source_height - bottom, source_height]

    target_x = [0, left, target_width - right, target_width]
    target_y = [0, top, target_height - bottom, target_height]

    result = Image.new("RGBA", size, (0, 0, 0, 0))

    for row in range(3):
        for column in range(3):

            patch = image.crop((
                source_x[column],
                source_y[row],
                source_x[column + 1],
                source_y[row + 1]
            ))

            patch_width = (
                target_x[column + 1] - target_x[column]
            )

            patch_height = (
                target_y[row + 1] - target_y[row]
            )

            if patch_width <= 0 or patch_height <= 0:
                continue

            if patch.size != (patch_width, patch_height):
                patch = patch.resize(
                    (patch_width, patch_height),
                    Image.Resampling.NEAREST
                )

            result.alpha_composite(
                patch,
                (target_x[column], target_y[row])
            )

    return result


# --------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------

def _clear():

    global _items, _images

    for item in _items:
        try:
            canvas.delete(item)
        except Exception:
            pass

    _items.clear()
    _images.clear()


def _cancel_hide_timer():

    global _hide_job

    if _hide_job is not None:
        try:
            root.after_cancel(_hide_job)
        except Exception:
            pass

        _hide_job = None


def hide():

    global _current_priority
    global _current_animation_text

    _cancel_hide_timer()
    _clear()

    _current_priority = -1
    _current_animation_text = None


def _wrap_text(text, font, max_width):

    words = str(text).split()
    lines = []
    current_line = ""

    for word in words:

        test_line = (
            f"{current_line} {word}".strip()
        )

        if font.measure(test_line) <= max_width:
            current_line = test_line

        else:
            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    return lines or [""]


# --------------------------------------------------
# MAIN DISPLAY FUNCTION
# --------------------------------------------------

def show(
    text,
    subtitle=None,
    image=None,
    rarity=None,
    duration=None,
    priority=0,
    font_size=FONT_SIZE,
    subtitle_size=SUBTITLE_SIZE,
    rarity_size=RARITY_SIZE
):
    """
    Display a speech bubble.

    text:
        Main message.

    subtitle:
        Optional second line, e.g. a hat name.

    image:
        Optional image path to display on the left.

    rarity:
        Optional rarity name. Uses the rarity colour.

    duration:
        Time in milliseconds. None means stay visible
        until hide() is called.

    priority:
        Higher priority notifications can replace
        lower priority notifications.

    x, y:
        Optional bubble centre coordinates.
    """

    global _hide_job
    global _current_priority

    if priority < _current_priority:
        return

    _cancel_hide_timer()
    _clear()

    _current_priority = priority

    # --------------------------------------------------
    # FONT AND TEXT MEASUREMENT
    # --------------------------------------------------

    main_font = tkfont.Font(
        root=root,
        family=FONT_FAMILY,
        size=font_size,
        weight="bold"
    )

    subtitle_font = tkfont.Font(
        root=root,
        family=FONT_FAMILY,
        size=subtitle_size
    )

    rarity_font = tkfont.Font(
        root=root,
        family=FONT_FAMILY,
        size=rarity_size,
        weight="bold"
    )

    has_image = image is not None

    text_max_width = MAX_TEXT_WIDTH

    main_lines = _wrap_text(
        text,
        main_font,
        text_max_width
    )

    subtitle_lines = []

    if subtitle:
        subtitle_lines = _wrap_text(
            subtitle,
            subtitle_font,
            text_max_width
        )

    main_width = max(
        main_font.measure(line)
        for line in main_lines
    )

    subtitle_width = max(
        (
            subtitle_font.measure(line)
            for line in subtitle_lines
        ),
        default=0
    )

    rarity_width = (
        rarity_font.measure(rarity)
        if rarity else 0
    )

    content_width = max(
        main_width,
        subtitle_width,
        rarity_width
    )

    image_width = (
        HAT_PREVIEW_SIZE[0] + 12
        if has_image else 0
    )

    content_width += image_width

    bubble_width = max(
        104,
        content_width + PADDING_X * 2
    )

    # --------------------------------------------------
    # CONTENT HEIGHT
    # --------------------------------------------------

    main_height = (
        len(main_lines) * main_font.metrics("linespace")
    )

    subtitle_height = (
        len(subtitle_lines) * subtitle_font.metrics("linespace")
    )

    rarity_height = (
        rarity_font.metrics("linespace")
        if rarity else 0
    )

    content_height = (
        main_height
        + subtitle_height
        + rarity_height
        + (4 if subtitle else 0)
        + (3 if rarity else 0)
    )

    content_height = max(
        content_height,
        HAT_PREVIEW_SIZE[1] if has_image else 0
    )

    bubble_height = max(
        65,
        content_height + PADDING_Y * 2 + 12
    )

    # --------------------------------------------------
    # LOAD AND RESIZE BUBBLE
    # --------------------------------------------------

    bubble = Image.open(
        BUBBLE_PATH
    ).convert("RGBA")

    bubble = resize_nine_slice(
        bubble,
        (bubble_width, bubble_height)
    )

    bubble_photo = ImageTk.PhotoImage(
        bubble,
        master=root
    )

    _images.append(bubble_photo)

    x = BUBBLE_X
    y = BUBBLE_Y

    # --------------------------------------------------
    # DRAW BUBBLE BACKGROUND
    # --------------------------------------------------

    bubble_item = canvas.create_image(
        x,
        y,
        image=bubble_photo,
        anchor="w",
        tags=("speech_bubble",)
    )

    _items.append(bubble_item)

    # --------------------------------------------------
    # CONTENT POSITIONS
    # --------------------------------------------------

    content_left = x + PADDING_X

    content_top = (
        y - bubble_height / 2 + PADDING_Y
    )

    # --------------------------------------------------
    # OPTIONAL IMAGE
    # --------------------------------------------------

    if has_image:

        preview = Image.open(
            image
        ).convert("RGBA")

        preview.thumbnail(
            HAT_PREVIEW_SIZE,
            Image.Resampling.NEAREST
        )

        preview_photo = ImageTk.PhotoImage(
            preview,
            master=root
        )

        _images.append(preview_photo)

        image_item = canvas.create_image(
            content_left + HAT_PREVIEW_SIZE[0] / 2,
            y,
            image=preview_photo,
            anchor="center",
            tags=("speech_bubble",)
        )

        _items.append(image_item)

        content_left += image_width

    # --------------------------------------------------
    # MAIN TEXT
    # --------------------------------------------------

    text_y = content_top

    main_item = canvas.create_text(
        content_left,
        text_y,
        text="\n".join(main_lines),
        anchor="nw",
        fill="#222222",
        font=main_font,
        tags=("speech_bubble",)
    )

    _items.append(main_item)

    text_y += main_height

    # --------------------------------------------------
    # SUBTITLE
    # --------------------------------------------------

    if subtitle:

        text_y += 4

        subtitle_item = canvas.create_text(
            content_left,
            text_y,
            text="\n".join(subtitle_lines),
            anchor="nw",
            fill="#222222",
            font=subtitle_font,
            tags=("speech_bubble",)
        )

        _items.append(subtitle_item)

        text_y += subtitle_height

    # --------------------------------------------------
    # RARITY
    # --------------------------------------------------

    if rarity:

        text_y += 3

        rarity_color = RARITIES.get(
            rarity,
            {}
        ).get("color", "#222222")

        rarity_item = canvas.create_text(
            content_left,
            text_y,
            text=rarity,
            anchor="nw",
            fill=rarity_color,
            font=rarity_font,
            tags=("speech_bubble",)
        )

        _items.append(rarity_item)

    # Keep the complete bubble above the duck.
    canvas.tag_raise("speech_bubble")

    # --------------------------------------------------
    # AUTOMATIC HIDE
    # --------------------------------------------------

    if duration is not None:

        def timed_hide():
            global _hide_job

            _hide_job = None
            hide()

        _hide_job = root.after(
            int(duration),
            timed_hide
        )


# --------------------------------------------------
# ANIMATION SUPPORT
# --------------------------------------------------

def show_animation_bubble(text):

    global _current_animation_text

    if not text:
        clear_animation_bubble()
        return

    # Support a single string or a list of dialogue options.
    if isinstance(text, list):
        if not text:
            clear_animation_bubble()
            return

        selected_text = random.choice(text)

    else:
        selected_text = text

    _current_animation_text = selected_text

    show(
        selected_text,
        duration=None,
        priority=1
    )


def clear_animation_bubble():
    global _current_priority
    global _current_animation_text

    if _current_priority <= 1:
        hide()
