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
DOG_INTERVAL = 3.0
MAX_DOGS = 8
DOG_SIZE = (54, 64)
DETECTION_RADIUS = 100
DEALER_SPEED = 180
DOG_SPEED = 45
DEALER_STARTING_LIVES = 3
INVULNERABILITY_DURATION = 2.0
INVULNERABILITY_BLINK_INTERVAL = 0.15
HEART_SIZE = (32, 32)
HEART_GAP = 6


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

    def draw(self, surface):
        if self.invulnerability_time > 0:
            blink_phase = int(
                self.invulnerability_time / INVULNERABILITY_BLINK_INTERVAL
            )
            if blink_phase % 2 == 0:
                return
        surface.blit(self.image, self.rect)


class Dog:
    """Enemigo que persigue al repartidor."""

    def __init__(self, image, start, destination):
        self.image = image
        self.rect = self.image.get_rect(topleft=start)
        self.position = pygame.Vector2(start)
        self.destination = pygame.Vector2(destination)
        self.is_entering = True
        self.speed = DOG_SPEED

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
        self.heart_image = pygame.transform.scale(
            self.load_image("heart.png"), HEART_SIZE
        )

        self.dealer = Dealer(dealer_image, 368, 440)
        self.dog_image = dog_image
        self.dogs = []
        self.time_since_last_dog = 0.0
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
        """Lanza una pizza al perro más cercano solo dentro del radio de detección."""
        if not self.dogs:
            return

        nearest_dog = min(
            self.dogs,
            key=lambda dog: pygame.Vector2(dog.rect.center)
            .distance_squared_to(self.dealer.rect.center),
        )
        distance_squared = pygame.Vector2(nearest_dog.rect.center).distance_squared_to(
            self.dealer.rect.center
        )
        if distance_squared > DETECTION_RADIUS**2:
            return

        self.pizzas.append(
            Pizza(self.pizza_image, self.dealer.rect.center, nearest_dog.rect.center)
        )

    def detect_hits(self):
        """Elimina cada perro y pizza que chocan, una vez por proyectil."""
        pizzas_survivors = []
        dogs_hit = []

        for pizza in self.pizzas:
            hit_dog = next(
                (
                    dog
                    for dog in self.dogs
                    if dog not in dogs_hit and pizza.rect.colliderect(dog.rect)
                ),
                None,
            )

            if hit_dog is None:
                pizzas_survivors.append(pizza)
            else:
                dogs_hit.append(hit_dog)

        self.pizzas = pizzas_survivors
        self.dogs = [dog for dog in self.dogs if dog not in dogs_hit]

    def detect_dog_collisions(self):
        """Quita los perros que tocan al repartidor y aplica daño si puede."""
        remaining_dogs = []
        for dog in self.dogs:
            if dog.rect.colliderect(self.dealer.rect):
                self.dealer.take_hit()
            else:
                remaining_dogs.append(dog)
        self.dogs = remaining_dogs

    def create_dog(self):
        """Crea un perro que entra desde un borde en una posición libre."""
        for _ in range(100):
            edge = random.choice(("top", "bottom", "left", "right"))
            if edge in ("top", "bottom"):
                x = random.randint(0, SCREEN_WIDTH - DOG_SIZE[0])
                y = 0 if edge == "top" else SCREEN_HEIGHT - DOG_SIZE[1]
                start_y = -DOG_SIZE[1] if edge == "top" else SCREEN_HEIGHT
                destination = (x, y)
                start = (x, start_y)
            else:
                y = random.randint(0, SCREEN_HEIGHT - DOG_SIZE[1])
                x = 0 if edge == "left" else SCREEN_WIDTH - DOG_SIZE[0]
                start_x = -DOG_SIZE[0] if edge == "left" else SCREEN_WIDTH
                destination = (x, y)
                start = (start_x, y)

            candidate = self.dog_image.get_rect(topleft=start)
            if all(not candidate.colliderect(dog.rect) for dog in self.dogs):
                destination_rect = self.dog_image.get_rect(topleft=destination)
                if all(
                    not destination_rect.colliderect(dog.rect)
                    for dog in self.dogs
                ):
                    self.dogs.append(Dog(self.dog_image, start, destination))
                    return True
        return False

    def update(self, delta_time):
        self.dealer.update(delta_time)

        # Aparece un perro cada tres segundos hasta alcanzar el máximo.
        if len(self.dogs) < MAX_DOGS:
            self.time_since_last_dog += delta_time
            if self.time_since_last_dog >= DOG_INTERVAL:
                # Si no hay un punto libre en este intento, se vuelve a intentar
                # en el siguiente fotograma sin perder el intervalo acumulado.
                if self.create_dog():
                    self.time_since_last_dog %= DOG_INTERVAL

        # Los perros entran desde el borde y luego persiguen al repartidor.
        for dog in self.dogs:
            was_entering = dog.is_entering
            previous_rect = dog.rect.copy()
            dog.update(self.dealer, delta_time)
            if was_entering and any(
                dog.rect.colliderect(other.rect)
                for other in self.dogs
                if other is not dog
            ):
                # Durante la entrada espera a que haya espacio; después puede
                # superponerse con otros perros mientras persigue al repartidor.
                dog.rect = previous_rect
                dog.position.update(previous_rect.topleft)
                dog.is_entering = True

        # El perro se elimina en el primer contacto, así no atraviesa al dealer.
        self.detect_dog_collisions()

        self.time_since_last_pizza += delta_time
        if self.time_since_last_pizza >= PIZZA_INTERVAL:
            self.time_since_last_pizza %= PIZZA_INTERVAL
            self.throw_pizza()

        for pizza in self.pizzas:
            pizza.update(delta_time)
        self.detect_hits()
        self.pizzas = [
            pizza for pizza in self.pizzas if not pizza.is_off_screen(self.bounds)
        ]

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.dealer.draw(self.screen)
        for life in range(self.dealer.lives):
            heart_rect = self.heart_image.get_rect(
                topleft=(10 + life * (HEART_SIZE[0] + HEART_GAP), 10)
            )
            self.screen.blit(self.heart_image, heart_rect)
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
