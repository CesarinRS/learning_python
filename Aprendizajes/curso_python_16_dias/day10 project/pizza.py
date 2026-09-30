import pygame

from config import PIZZA_SPEED

class Pizza:
    """Proyectil que viaja en línea recta a velocidad constante."""

    def __init__(self, image, start, target):
        self.image = image
        self.rect = self.image.get_rect(center=start)
        self.position = pygame.Vector2(self.rect.center)
        direction = pygame.Vector2(target) - self.position
        self.direction = direction.normalize() if direction.length_squared() else direction

    def update(self, delta_time):
        self.position += self.direction * PIZZA_SPEED * delta_time
        self.rect.center = round(self.position.x), round(self.position.y)

    def is_off_screen(self, bounds):
        return not bounds.colliderect(self.rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
