from pathlib import Path

import pygame

from config import (
    DETECTION_RADIUS,
    ENEMY_INTERVAL,
    FPS,
    HEART_GAP,
    HEART_SIZE,
    MAX_ENEMIES,
    PIZZA_INTERVAL,
    PIZZA_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from cat import Cat
from dealer import Dealer
from dog import Dog
from enemy import Enemy
from pizza import Pizza
from power_ups import PizzaBox, PowerUpManager


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
        self.image_dir = self.asset_dir / "assets" / "images"
        self.soundtrack_dir = self.asset_dir / "assets" / "soundtrack"
        self.score_font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 80)
        pygame.mixer.music.load(self.soundtrack_dir / "Soundtrack.mp3")
        pygame.mixer.music.set_volume(0.25)
        self.shoot_sound = pygame.mixer.Sound(self.soundtrack_dir / "Shoot.mp3")
        self.hit_sound = pygame.mixer.Sound(self.soundtrack_dir / "Hit.mp3")
        self.life_lost_sound = pygame.mixer.Sound(
            self.soundtrack_dir / "life_lost.mp3"
        )

        icon = self.load_image("icon.png")
        pygame.display.set_icon(icon)
        self.background = pygame.transform.scale(
            self.load_image("background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        dealer_image = pygame.transform.scale(
            self.load_image("repartidor.png"), (64, 100)
        )
        self.pizza_image = pygame.transform.scale(
            self.load_image("pizza.png"), PIZZA_SIZE
        )
        self.heart_image = pygame.transform.scale(
            self.load_image("heart.png"), HEART_SIZE
        )
        self.power_ups = PowerUpManager(
            PizzaBox.load_image(self.image_dir), self.bounds
        )

        self.dealer = Dealer(dealer_image, 368, 440)
        self.enemies = []
        self.score = 0
        self.state = "playing"
        self.elapsed_time = 0.0
        self.time_since_last_enemy = 0.0
        self.pizzas = []
        self.time_since_last_pizza = 0.0

    def load_image(self, filename):
        """Carga una imagen desde la carpeta de imágenes del proyecto."""
        return pygame.image.load(self.image_dir / filename)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.dealer.handle_key(event.key, event.type == pygame.KEYDOWN)
        return True

    def throw_pizza(self):
        """Lanza una pizza al enemigo más cercano dentro del radio de detección."""
        if not self.enemies:
            return

        nearest_enemy = min(
            self.enemies,
            key=lambda enemy: pygame.Vector2(enemy.rect.center)
            .distance_squared_to(self.dealer.rect.center),
        )
        distance_squared = pygame.Vector2(
            nearest_enemy.rect.center
        ).distance_squared_to(self.dealer.rect.center)
        if distance_squared > DETECTION_RADIUS**2:
            return

        self.pizzas.append(
            Pizza(self.pizza_image, self.dealer.rect.center, nearest_enemy.rect.center)
        )
        self.shoot_sound.play()

    def detect_hits(self):
        """Elimina cada enemigo y pizza que chocan, una vez por proyectil."""
        pizzas_survivors = []
        enemies_hit = []

        for pizza in self.pizzas:
            hit_enemy = next(
                (
                    enemy
                    for enemy in self.enemies
                    if enemy not in enemies_hit and pizza.rect.colliderect(enemy.rect)
                ),
                None,
            )

            if hit_enemy is None:
                pizzas_survivors.append(pizza)
            else:
                enemies_hit.append(hit_enemy)

        self.pizzas = pizzas_survivors
        self.enemies = [enemy for enemy in self.enemies if enemy not in enemies_hit]
        self.score += len(enemies_hit)
        for _enemy in enemies_hit:
            self.hit_sound.play()

    def detect_enemy_collisions(self):
        """Quita los enemigos que tocan al repartidor y aplica daño si puede."""
        remaining_enemies = []
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.dealer.rect):
                if self.dealer.take_hit():
                    self.life_lost_sound.play()
                    self.power_ups.notify_life_lost()
            else:
                remaining_enemies.append(enemy)
        self.enemies = remaining_enemies

    def create_enemy(self):
        """Delegación de la creación del enemigo al módulo Enemy."""
        enemy = Enemy.create_random(
            self.bounds, self.enemies, self.image_dir, (Dog, Cat)
        )
        if enemy is None:
            return False
        self.enemies.append(enemy)
        return True

    def update(self, delta_time):
        if self.state == "finished":
            return

        self.elapsed_time += delta_time
        self.dealer.update(delta_time)

        if len(self.enemies) < MAX_ENEMIES:
            self.time_since_last_enemy += delta_time
            if (
                self.time_since_last_enemy >= ENEMY_INTERVAL
                and self.create_enemy()
            ):
                self.time_since_last_enemy %= ENEMY_INTERVAL

        for enemy in self.enemies:
            was_entering = enemy.is_entering
            previous_rect = enemy.rect.copy()
            enemy.update(self.dealer, delta_time)
            if was_entering and any(
                enemy.rect.colliderect(other.rect)
                for other in self.enemies
                if other is not enemy
            ):
                enemy.rect = previous_rect
                enemy.position.update(previous_rect.topleft)
                enemy.is_entering = True

        self.detect_enemy_collisions()
        if self.dealer.lives == 0:
            self.state = "finished"
            pygame.mixer.music.stop()
            return

        self.power_ups.update(delta_time, self.dealer)

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
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.power_ups.draw(self.screen)
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
