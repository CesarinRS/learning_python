import random
from pathlib import Path

import pygame


class PizzaBox:
    """Caja de pizza que recupera una vida y se desvanece al expirar."""

    IMAGE_FILE = "pizza_box.png"
    SIZE = (48, 48)
    LIFETIME = 5.0
    FADE_DURATION = 1.0

    def __init__(self, image, bounds):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            random.randint(bounds.left, bounds.right - self.rect.width),
            random.randint(bounds.top, bounds.bottom - self.rect.height),
        )
        self.age = 0.0

    @classmethod
    def load_image(cls, image_dir):
        image = pygame.image.load(Path(image_dir) / cls.IMAGE_FILE)
        return pygame.transform.scale(image, cls.SIZE)

    def update(self, delta_time):
        self.age += delta_time
        return self.age < self.LIFETIME

    def draw(self, surface):
        remaining = self.LIFETIME - self.age
        if remaining <= self.FADE_DURATION:
            alpha = round(255 * max(0.0, remaining / self.FADE_DURATION))
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        surface.blit(self.image, self.rect)


class PowerUpManager:
    """Controla los tiempos, apariciones y recolección de cajas de pizza."""

    MAX_APPEARANCES = 5
    INITIAL_DELAY = 5.0
    MIN_SPAWN_INTERVAL = 15.0
    MAX_SPAWN_INTERVAL = 20.0

    def __init__(self, image, bounds):
        self.image = image
        self.bounds = bounds
        self.active_power_up = None
        self.appearances = 0
        self.has_lost_life = False
        self.time_until_spawn = None

    def notify_life_lost(self):
        """Activa las apariciones tras una pérdida y espera cinco segundos."""
        if self.appearances >= self.MAX_APPEARANCES:
            return
        self.has_lost_life = True
        if self.active_power_up is None:
            self.time_until_spawn = self.INITIAL_DELAY

    def update(self, delta_time, dealer):
        if self.active_power_up is not None:
            is_alive = self.active_power_up.update(delta_time)
            if (
                is_alive
                and self.active_power_up.rect.colliderect(dealer.rect)
                and dealer.recover_life()
            ):
                self.active_power_up = None
                self._schedule_next_spawn()
            elif not is_alive:
                self.active_power_up = None
                self._schedule_next_spawn()
            return

        if not self.has_lost_life or self.time_until_spawn is None:
            return

        self.time_until_spawn -= delta_time
        if self.time_until_spawn <= 0:
            self.active_power_up = PizzaBox(self.image, self.bounds)
            self.appearances += 1
            self.time_until_spawn = None

    def _schedule_next_spawn(self):
        if self.appearances < self.MAX_APPEARANCES:
            self.time_until_spawn = random.uniform(
                self.MIN_SPAWN_INTERVAL, self.MAX_SPAWN_INTERVAL
            )

    def draw(self, surface):
        if self.active_power_up is not None:
            self.active_power_up.draw(surface)
