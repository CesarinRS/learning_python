import pygame

from config import (
    DEALER_SPEED,
    DEALER_MAX_LIVES,
    DEALER_STARTING_LIVES,
    INVULNERABILITY_BLINK_INTERVAL,
    INVULNERABILITY_DURATION,
)


class Dealer:
    """Jugador que se mueve y lanza pizzas."""

    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = DEALER_SPEED
        self.direction = pygame.Vector2()
        self.pressed_keys = set()
        self.lives = DEALER_STARTING_LIVES
        self.invulnerability_time = 0.0

    def handle_key(self, key, pressed):
        """Actualiza la dirección según las teclas que siguen presionadas."""
        if pressed:
            self.pressed_keys.add(key)
        else:
            self.pressed_keys.discard(key)

        self.direction.x = (
            int(pygame.K_RIGHT in self.pressed_keys)
            - int(pygame.K_LEFT in self.pressed_keys)
        )
        self.direction.y = (
            int(pygame.K_DOWN in self.pressed_keys)
            - int(pygame.K_UP in self.pressed_keys)
        )

        # Normalizar evita que el movimiento diagonal sea más rápido.
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

    def update(self, delta_time):
        self.invulnerability_time = max(0.0, self.invulnerability_time - delta_time)
        self.rect.x += round(self.direction.x * self.speed * delta_time)
        self.rect.y += round(self.direction.y * self.speed * delta_time)
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def take_hit(self):
        """Quita una vida si el repartidor no está temporalmente protegido."""
        if self.invulnerability_time > 0:
            return False

        self.lives = max(0, self.lives - 1)
        self.invulnerability_time = INVULNERABILITY_DURATION
        return True

    def recover_life(self):
        """Recupera una vida hasta el máximo permitido."""
        if self.lives >= DEALER_MAX_LIVES:
            return False
        self.lives += 1
        return True

    def draw(self, surface):
        if self.invulnerability_time > 0:
            blink_phase = int(
                self.invulnerability_time / INVULNERABILITY_BLINK_INTERVAL
            )
            if blink_phase % 2 == 0:
                return
        surface.blit(self.image, self.rect)