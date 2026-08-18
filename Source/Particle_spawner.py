import random
from Source.Window_Manager import canvas
from Source.Config.paths import PARTICLES_DIR
from PIL import Image, ImageTk
import os
import math


PARTICLE_SPAWN_PADDING = 20


def load_particle_images(folder_name):
    folder = os.path.join(PARTICLES_DIR, folder_name)

    return [
        ImageTk.PhotoImage(
            Image.open(os.path.join(folder, filename))
        )
        for filename in sorted(os.listdir(folder))
        if (
            filename.lower().endswith(".png")
            and filename.lower() != "bubble_pop.png"
        )
    ]


def load_particle_pop(folder_name):
    folder = os.path.join(PARTICLES_DIR, folder_name)

    path = os.path.join(
        folder,
        "bubble_pop.png"
    )

    if not os.path.exists(path):
        return None

    return ImageTk.PhotoImage(
        Image.open(path)
    )


class Particle:

    def __init__(self, x, y, image, pop_image):
        self.id = canvas.create_image(
            x,
            y,
            image=image
        )

        self.image = image
        self.pop_image = pop_image

        self.width = image.width()
        self.height = image.height()

        self.wave_strength = random.uniform(0, 1)
        self.angle = random.uniform(0,math.pi * 2)

        canvas.tag_lower(self.id)

        self.speed_y = random.uniform(0.5,2)

        self.distance_left = random.uniform(
            canvas.winfo_height() * 0.6,
            canvas.winfo_height() * 0.9
        )


    def move(self):

        self.angle += 0.1

        self.distance_left -= self.speed_y

        if self.distance_left <= 0:

            self.pop()

            return False


        canvas.move(
            self.id,
            math.sin(self.angle) * self.wave_strength,
            -self.speed_y
        )


        x, y = canvas.coords(self.id)

        half_width = self.width / 2
        half_height = self.height / 2


        if (
            y - half_height <= 0
            or
            x - half_width <= 0
            or
            x + half_width >= canvas.winfo_width()
        ):

            self.destroy()

            return False


        return True


    def pop(self):

        x, y = canvas.coords(
            self.id
        )

        self.destroy()


        if self.pop_image is None:
            return


        pop_id = canvas.create_image(
            x,
            y,
            image=self.pop_image
        )


        canvas.tag_lower(pop_id)


        canvas.after(
            100,
            lambda: canvas.delete(pop_id)
        )


    def destroy(self):

        canvas.delete(
            self.id
        )


class ParticleManager:

    def __init__(self, images, pop_image):

        self.particles = []

        self.images = images

        self.pop_image = pop_image

        self.running = True


    def spawn(self):

        if not self.running:
            return


        canvas_width = canvas.winfo_width()


        if canvas_width <= PARTICLE_SPAWN_PADDING * 2:
            return


        x = random.randint(
            PARTICLE_SPAWN_PADDING,
            canvas_width - PARTICLE_SPAWN_PADDING
        )


        y = canvas.winfo_height()


        self.particles.append(
            Particle(
                x,
                y,
                random.choice(self.images),
                self.pop_image
            )
        )


    def update(self):

        if not self.running:
            return


        self.particles = [
            particle
            for particle in self.particles
            if particle.move()
        ]


        canvas.after(30,self.update)


    def auto_spawn(self):

        if not self.running:
            return


        self.spawn()


        canvas.after(
            random.randint(300,1000),
            self.auto_spawn
        )


    def stop(self):

        self.running = False


        for particle in self.particles:
            particle.destroy()


        self.particles.clear()


class ParticleSystem:

    def __init__(self):

        self.particles = {}


    def enable(self, name):

        if name in self.particles:
            return


        images = load_particle_images(name)


        pop_image = load_particle_pop(name)


        manager = ParticleManager(
            images,
            pop_image
        )


        self.particles[name] = manager


        manager.update()

        manager.auto_spawn()


    def disable(self, name):

        if name in self.particles:

            self.particles[name].stop()

            del self.particles[name]


    def toggle(self, name, enabled):

        if enabled:
            self.enable(name)

        else:
            self.disable(name)


    def set_disabled(self, name, disabled):

        if disabled:
            self.disable(name)

        else:
            self.enable(name)


    def disable_all(self):

        for manager in self.particles.values():
            manager.stop()

        self.particles.clear()