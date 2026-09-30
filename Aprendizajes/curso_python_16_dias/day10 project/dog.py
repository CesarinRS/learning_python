import pygame

from enemy import Enemy

from config import DOG_SPEED


class Dog(Enemy):
    """Enemy that enters from an edge and then chases the dealer."""

    speed = DOG_SPEED

    def __init__(self, image, start, destination):
        super().__init__(image, start)
        self.position = pygame.Vector2(start)
        self.destination = pygame.Vector2(destination)
        self.is_entering = True

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
