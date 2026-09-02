import random
import time

from dataclasses import dataclass


# ============================================================
# CONFIG
# ============================================================

BASE_SCALE = 1.0

GROW_SCALE = 1.5

GROW_DURATION = 8.0
SHRINK_DURATION = 8.0

# Minimum / maximum time the duck stays giant.
GIANT_TIME = (60, 120)


# ============================================================
# EFFECT
# ============================================================

@dataclass
class Effect:

    name: str

    # Effect start time.
    start_time: float

    # Extra information an effect may need.
    data: dict


# ============================================================
# EFFECT MANAGER
# ============================================================

class EffectManager:

    def __init__(self, root, get_current_animation, play_animation):

        self.root = root

        # Functions supplied by animation.py.
        #
        # This avoids creating a circular import.
        self.get_current_animation = get_current_animation
        self.play_animation = play_animation

        # Currently active effect.
        self.active_effect = None

        # ----------------------------------------------------
        # Duck transform
        # ----------------------------------------------------

        self.scale = BASE_SCALE

        # ----------------------------------------------------
        # Scaling animation
        # ----------------------------------------------------

        self.scale_start = BASE_SCALE
        self.scale_target = BASE_SCALE

        self.scale_start_time = 0.0
        self.scale_duration = 0.0
        self.grow_state = None

    # ========================================================
    # GENERAL EFFECT SYSTEM
    # ========================================================

    def start(self, effect_name):

        """
        Start an effect by name.

        This is the central place where new effects can
        eventually be registered.
        """

        if effect_name == "grow":

            self.start_grow()

            return True

        return False

    # ========================================================
    # SCALE
    # ========================================================

    def start_scale(self, target, duration):

        self.scale_start = self.scale
        self.scale_target = target

        self.scale_start_time = time.monotonic()
        self.scale_duration = duration

    def update_scale(self):

        if self.scale_duration <= 0:

            self.scale = self.scale_target

            return True

        elapsed = (
            time.monotonic()
            - self.scale_start_time
        )

        progress = min(
            elapsed / self.scale_duration,
            1.0
        )

        # Smooth ease in/out.
        progress = (
            progress
            * progress
            * (3 - 2 * progress)
        )

        self.scale = (
            self.scale_start
            + (
                self.scale_target
                - self.scale_start
            )
            * progress
        )

        return progress >= 1.0

    # ========================================================
    # GROW
    # ========================================================

    def start_grow(self):

        # Don't allow another grow effect to start while
        # one is already active.
        if self.grow_state is not None:
            return

        self.grow_state = "growing"

        self.active_effect = Effect(
            name="grow",
            start_time=time.monotonic(),
            data={}
        )

        self.start_scale(
            target=GROW_SCALE,
            duration=GROW_DURATION
        )

    def update_grow(self):

        if self.active_effect is None:
            return

        finished = self.update_scale()

        if not finished:
            return

        # ----------------------------------------------------
        # Finished growing
        # ----------------------------------------------------

        if self.grow_state == "growing":

            self.grow_state = "giant"

            duration = random.uniform(
                GIANT_TIME[0],
                GIANT_TIME[1]
            )

            self.root.after(
                int(duration * 1000),
                self.request_shrink
            )

            return

        # ----------------------------------------------------
        # Finished shrinking
        # ----------------------------------------------------

        if self.grow_state == "shrinking":

            self.finish_grow()

    # ========================================================
    # SHRINK
    # ========================================================

    def request_shrink(self):

        # The effect may already have ended.
        if self.grow_state != "giant":
            return

        if self.get_current_animation() != "Idle":

            self.root.after(
                200,
                self.request_shrink
            )

            return

        self.grow_state = "shrinking"

        self.start_scale(
            target=BASE_SCALE,
            duration=SHRINK_DURATION
        )

    # ========================================================
    # FINISH GROW
    # ========================================================

    def finish_grow(self):

        self.scale = BASE_SCALE

        self.grow_state = None

        self.active_effect = None

        self.play_animation("Idle")

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        """
        Called every animation frame.
        """

        if self.active_effect is None:
            return

        if self.active_effect.name == "grow":

            self.update_grow()