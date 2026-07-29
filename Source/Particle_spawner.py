import random
from Source.Window_Manager import canvas
from Source.Config.paths import PARTICLES_DIR
from PIL import Image, ImageTk
import os
import math


def load_particle_images(folder_name):
    folder = os.path.join(PARTICLES_DIR, folder_name)

    return [
        ImageTk.PhotoImage(
            Image.open(os.path.join(folder, filename))
        )
        for filename in sorted(os.listdir(folder))
        if filename.lower().endswith(".png")
    ]


class Particle:

    def __init__(self, x, y, image):
        self.id = canvas.create_image(x, y, image=image)
        self.image = image
        self.width = image.width()
        self.height = image.height()

        self.wave_strength = random.uniform(0, 1)
        self.angle = random.uniform(0, math.pi * 2)

        canvas.tag_lower(self.id)

        self.speed_y = random.uniform(0.5, 2)


        self.distance_left = random.uniform(100, 500)


    def move(self):
        self.angle += 0.1

        self.distance_left -= self.speed_y

        if self.distance_left <= 0:
            self.destroy()
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
            y - half_height <= 0 or
            x - half_width <= 0 or
            x + half_width >= canvas.winfo_width()
        ):
            self.destroy()
            return False

        return True

    def destroy(self):
        canvas.delete(self.id)



class ParticleManager:

    def __init__(self, images):
        self.particles = []
        self.images = images
        self.running = True


    def spawn(self):
        if not self.running:
            return

        x = random.randint(0, canvas.winfo_width())
        y = canvas.winfo_height()

        self.particles.append(
            Particle(x, y, random.choice(self.images))
        )


    def update(self):
        if not self.running:
            return

        self.particles = [
            particle
            for particle in self.particles
            if particle.move()
        ]

        canvas.after(
            30,
            self.update
        )


    def auto_spawn(self):
        if not self.running:
            return

        self.spawn()

        canvas.after(
            random.randint(300, 1000),
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

        manager = ParticleManager(
            load_particle_images(name)
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