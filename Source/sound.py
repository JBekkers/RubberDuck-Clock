import os
import pygame
from Source.Config.paths import SOUNDS_DIR
import math

pygame.mixer.init()

sound_volume = 100


def set_sound_volume(volume):
    global sound_volume

    sound_volume = int(volume)


def play_sound(filename):

    if sound_volume <= 0:
        return

    path = os.path.join(
        SOUNDS_DIR,
        filename
    )

    if not os.path.exists(path):
        return

    sound = pygame.mixer.Sound(path)

    sound.set_volume(
        math.pow(sound_volume / 100, 2)
    )

    sound.play()