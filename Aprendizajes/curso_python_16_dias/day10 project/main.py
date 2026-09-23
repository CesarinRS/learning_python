import random
from pathlib import Path

import pygame


# Configuración de la ventana y del juego.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PIZZA_SIZE = (32, 32)
PIZZA_INTERVAL = 1.0
PIZZA_SPEED = 300  # Píxeles por segundo.


class Dealer:
    """Jugador que se mueve y lanza pizzas."""

    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 120  # Equivale a los 2 píxeles por fotograma originales.
        self.direction = pygame.Vector2()
        self.pressed_keys = set()

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
        self.rect.x += round(self.direction.x * self.speed * delta_time)
        self.rect.y += round(self.direction.y * self.speed * delta_time)
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Dog:
    """Enemigo que persigue al repartidor."""

    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 22.8  # Equivale a 0.38 píxeles por fotograma.

    def update(self, target, delta_time):
        direction = pygame.Vector2(target.rect.center) - self.rect.center
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.rect.x += round(direction.x * self.speed * delta_time)
            self.rect.y += round(direction.y * self.speed * delta_time)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


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


class PizzaSurvivor:
    """Coordina recursos, entidades y el ciclo principal del juego."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pizza Simulator")
        self.clock = pygame.time.Clock()
        self.bounds = self.screen.get_rect()
        self.asset_dir = Path(__file__).resolve().parent

        self.icon = self.load_image("icon.png")
        pygame.display.set_icon(self.icon)
        self.background = pygame.transform.scale(
            self.load_image("background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        dealer_image = pygame.transform.scale(
            self.load_image("repartidor.png"), (64, 100)
        )
        dog_image = pygame.transform.scale(self.load_image("dog.png"), (54, 64))
        self.pizza_image = pygame.transform.scale(
            self.load_image("pizza.png"), PIZZA_SIZE
        )

        self.dealer = Dealer(dealer_image, 368, 440)
        self.dogs = [Dog(dog_image, random.randint(0, SCREEN_WIDTH - 54), 0)]
        self.pizzas = []
        self.time_since_last_pizza = 0.0

    def load_image(self, filename):
        """Carga una imagen desde la carpeta del proyecto."""
        return pygame.image.load(self.asset_dir / filename)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.dealer.handle_key(event.key, event.type == pygame.KEYDOWN)
        return True

    def throw_pizza(self):
        """Lanza una pizza hacia el perro más cercano al repartidor."""
        if not self.dogs:
            return

        nearest_dog = min(
            self.dogs,
            key=lambda dog: pygame.Vector2(dog.rect.center)
            .distance_squared_to(self.dealer.rect.center),
        )
        self.pizzas.append(
            Pizza(self.pizza_image, self.dealer.rect.center, nearest_dog.rect.center)
        )

    def update(self, delta_time):
        self.dealer.update(delta_time)
        for dog in self.dogs:
            dog.update(self.dealer, delta_time)

        self.time_since_last_pizza += delta_time
        if self.time_since_last_pizza >= PIZZA_INTERVAL:
            self.time_since_last_pizza %= PIZZA_INTERVAL
            self.throw_pizza()

        for pizza in self.pizzas:
            pizza.update(delta_time)
        self.pizzas = [
            pizza for pizza in self.pizzas if not pizza.is_off_screen(self.bounds)
        ]

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.dealer.draw(self.screen)
        for dog in self.dogs:
            dog.draw(self.screen)
        for pizza in self.pizzas:
            pizza.draw(self.screen)
        pygame.display.flip()

    def run(self):
        playing = True
        while playing:
            delta_time = self.clock.tick(FPS) / 1000
            playing = self.handle_events()
            self.update(delta_time)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = PizzaSurvivor()
    game.run()
