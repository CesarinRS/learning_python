import random
from pathlib import Path

import pygame

from config import (
    DETECTION_RADIUS,
    DOG_INTERVAL,
    DOG_SIZE,
    FPS,
    HEART_GAP,
    HEART_SIZE,
    MAX_DOGS,
    PIZZA_INTERVAL,
    PIZZA_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from dealer import Dealer
from dog import Dog
from pizza import Pizza


class PizzaSurvivor:
    """Coordina recursos, entidades y el ciclo principal del juego."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pizza Simulator")
        self.clock = pygame.time.Clock()
        self.bounds = self.screen.get_rect()
        self.asset_dir = Path(__file__).resolve().parent
        self.score_font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 80)
        pygame.mixer.music.load(self.asset_dir / "Soundtrack.mp3")
        pygame.mixer.music.set_volume(0.25)
        self.shoot_sound = pygame.mixer.Sound(self.asset_dir / "Shoot.mp3")
        self.hit_sound = pygame.mixer.Sound(self.asset_dir / "Hit.mp3")
        self.life_lost_sound = pygame.mixer.Sound(self.asset_dir / "life_lost.mp3")

        icon = self.load_image("icon.png")
        pygame.display.set_icon(icon)
        self.background = pygame.transform.scale(
            self.load_image("background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        dealer_image = pygame.transform.scale(
            self.load_image("repartidor.png"), (64, 100)
        )
        self.dog_image = pygame.transform.scale(
            self.load_image("dog.png"), DOG_SIZE
        )
        self.pizza_image = pygame.transform.scale(
            self.load_image("pizza.png"), PIZZA_SIZE
        )
        self.heart_image = pygame.transform.scale(
            self.load_image("heart.png"), HEART_SIZE
        )

        self.dealer = Dealer(dealer_image, 368, 440)
        self.dogs = []
        self.score = 0
        self.state = "playing"
        self.elapsed_time = 0.0
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
        """Lanza una pizza al perro más cercano dentro del radio de detección."""
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
        self.shoot_sound.play()

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
        self.score += len(dogs_hit)
        for _dog in dogs_hit:
            self.hit_sound.play()

    def detect_dog_collisions(self):
        """Quita los perros que tocan al repartidor y aplica daño si puede."""
        remaining_dogs = []
        for dog in self.dogs:
            if dog.rect.colliderect(self.dealer.rect):
                if self.dealer.take_hit():
                    self.life_lost_sound.play()
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
                if all(not destination_rect.colliderect(dog.rect) for dog in self.dogs):
                    self.dogs.append(Dog(self.dog_image, start, destination))
                    return True
        return False

    def update(self, delta_time):
        if self.state == "finished":
            return

        self.elapsed_time += delta_time
        self.dealer.update(delta_time)

        if len(self.dogs) < MAX_DOGS:
            self.time_since_last_dog += delta_time
            if self.time_since_last_dog >= DOG_INTERVAL and self.create_dog():
                self.time_since_last_dog %= DOG_INTERVAL

        for dog in self.dogs:
            was_entering = dog.is_entering
            previous_rect = dog.rect.copy()
            dog.update(self.dealer, delta_time)
            if was_entering and any(
                dog.rect.colliderect(other.rect)
                for other in self.dogs
                if other is not dog
            ):
                dog.rect = previous_rect
                dog.position.update(previous_rect.topleft)
                dog.is_entering = True

        self.detect_dog_collisions()
        if self.dealer.lives == 0:
            self.state = "finished"
            pygame.mixer.music.stop()
            return

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
        self.score_drawer()
        for dog in self.dogs:
            dog.draw(self.screen)
        for pizza in self.pizzas:
            pizza.draw(self.screen)
        if self.state == "finished":
            self.draw_game_over()
        pygame.display.flip()

    def score_drawer(self):
        """Dibuja el puntaje actual en la esquina superior derecha."""
        label = "Score: "
        gradient_start = (255, 0, 0)
        gradient_end = (0, 0, 0)
        x, y = 650, 10

        for index, character in enumerate(label):
            blend = index / max(1, len(label) - 1)
            color = tuple(
                round(start + (end - start) * blend)
                for start, end in zip(gradient_start, gradient_end)
            )
            character_surface = self.score_font.render(character, True, color)
            self.screen.blit(character_surface, (x, y))
            x += character_surface.get_width()

        score_surface = self.score_font.render(str(self.score), True, gradient_end)
        self.screen.blit(score_surface, (x, y))

        minutes, seconds = divmod(int(self.elapsed_time), 60)
        time_text = f"Time: {minutes}:{seconds:02d}"
        time_width = self.score_font.size(time_text)[0]
        time_x = 650 + (x + score_surface.get_width() - 650 - time_width) // 2
        self.draw_gradient_text(time_text, time_x, y + self.score_font.get_linesize())

    def draw_gradient_text(self, text, x, y, font=None, phase=0.0):
        """Dibuja texto con un degradado rojo y negro desplazable."""
        gradient_start = (255, 0, 0)
        gradient_end = (0, 0, 0)
        font = font or self.score_font
        for index, character in enumerate(text):
            blend = (index / max(1, len(text) - 1) + phase) % 1.0
            color = tuple(
                round(start + (end - start) * blend)
                for start, end in zip(gradient_start, gradient_end)
            )
            character_surface = font.render(character, True, color)
            self.screen.blit(character_surface, (x, y))
            x += character_surface.get_width()

    def draw_game_over(self):
        """Dibuja el resultado final con un degradado animado."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 150))
        self.screen.blit(overlay, (0, 0))

        animation_time = pygame.time.get_ticks() / 1000
        title = "GAME OVER"
        title_width = self.game_over_font.size(title)[0]
        title_x = (SCREEN_WIDTH - title_width) // 2
        title_y = SCREEN_HEIGHT // 2 - 100
        phase = (animation_time * 0.5) % 1.0
        self.draw_gradient_text(title, title_x, title_y, self.game_over_font, phase)

        minutes, seconds = divmod(int(self.elapsed_time), 60)
        final_lines = (
            f"Score: {self.score}",
            f"Time: {minutes}:{seconds:02d}",
        )
        line_y = title_y + self.game_over_font.get_linesize() + 12
        for line in final_lines:
            line_width = self.score_font.size(line)[0]
            line_x = (SCREEN_WIDTH - line_width) // 2
            self.draw_gradient_text(line, line_x, line_y)
            line_y += self.score_font.get_linesize()

    def run(self):
        pygame.mixer.music.play(-1)
        playing = True
        try:
            while playing:
                delta_time = self.clock.tick(FPS) / 1000
                playing = self.handle_events()
                self.update(delta_time)
                self.draw()
        finally:
            pygame.quit()
