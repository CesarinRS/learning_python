import random
from pathlib import Path

import pygame


class Enemy:
    """Comportamiento compartido y creación aleatoria de enemigos."""

    image_file = None
    size = None
    speed = 0
    _image_cache = {}

    def __init__(self, image, start, destination):
        self.image = image
        self.rect = self.image.get_rect(topleft=start)
        self.position = pygame.Vector2(start)
        self.destination = pygame.Vector2(destination)
        self.speed = type(self).speed
        self.is_entering = True

    @classmethod
    def load_image(cls, asset_dir):
        if cls not in Enemy._image_cache:
            image_path = Path(asset_dir) / cls.image_file
            image = pygame.image.load(image_path)
            Enemy._image_cache[cls] = pygame.transform.scale(image, cls.size)
        return Enemy._image_cache[cls]

    @classmethod
    def create_random(cls, bounds, existing_enemies, asset_dir, enemy_types):
        """Crea un subtipo registrado en un borde sin superponer otro enemigo."""
        if not enemy_types:
            raise RuntimeError("No hay tipos de enemigos registrados.")

        enemy_type = random.choice(enemy_types)
        image = enemy_type.load_image(asset_dir)
        width, height = enemy_type.size

        for _ in range(100):
            edge = random.choice(("top", "bottom", "left", "right"))
            if edge in ("top", "bottom"):
                x = random.randint(bounds.left, bounds.right - width)
                y = bounds.top if edge == "top" else bounds.bottom - height
                start_y = bounds.top - height if edge == "top" else bounds.bottom
                destination = (x, y)
                start = (x, start_y)
            else:
                y = random.randint(bounds.top, bounds.bottom - height)
                x = bounds.left if edge == "left" else bounds.right - width
                start_x = bounds.left - width if edge == "left" else bounds.right
                destination = (x, y)
                start = (start_x, y)

            candidate = image.get_rect(topleft=start)
            destination_rect = image.get_rect(topleft=destination)
            if all(
                not candidate.colliderect(enemy.rect)
                and not destination_rect.colliderect(enemy.rect)
                for enemy in existing_enemies
            ):
                return enemy_type(image, start, destination)
        return None

    def update(self, target, delta_time):
        if self.is_entering:
            offset = self.destination - self.position
            distance = offset.length()
            step = self.speed * delta_time
            if distance <= step:
                self.position = self.destination.copy()
                self.is_entering = False
            elif distance > 0:
                self.position += offset.normalize() * step
            self.rect.topleft = round(self.position.x), round(self.position.y)
            return

        direction = pygame.Vector2(target.rect.center) - self.rect.center
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.rect.x += round(direction.x * self.speed * delta_time)
            self.rect.y += round(direction.y * self.speed * delta_time)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
