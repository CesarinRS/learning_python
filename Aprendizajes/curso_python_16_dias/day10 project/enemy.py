import pygame


class Enemy:
    """Base class for enemies with a shared image, rect, and draw method."""

    def __init__(self, image, start):
        self.image = image
        self.rect = self.image.get_rect(topleft=start)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
