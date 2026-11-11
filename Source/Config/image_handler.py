
from functools import lru_cache
from PIL import Image, ImageTk


@lru_cache(maxsize=64)
def get_hat_thumbnail(path, size=(68, 68)):
    with Image.open(path) as source:
        image = source.convert("RGBA")

    # Crop away transparent pixels around the hat.
    bbox = image.getbbox()

    if bbox:
        image = image.crop(bbox)

    # Resize the cropped hat while preserving its proportions.
    image.thumbnail(
        size,
        Image.Resampling.NEAREST
    )

    return ImageTk.PhotoImage(image)
