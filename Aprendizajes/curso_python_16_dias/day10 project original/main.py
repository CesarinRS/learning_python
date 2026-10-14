import pygame
from pathlib import Path
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(Path(__file__).parent / 'assets' / 'img' /'ufo_icon.png')
pygame.display.set_icon(icon)
fondo = pygame.image.load(Path(__file__).parent / 'assets' / 'img' / 'Fondo.jpg')

# Add soundtrack
mixer.music.load(Path(__file__).parent / 'assets' / 'sounds' / 'MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
shoot_sound = mixer.Sound(
    Path(__file__).parent / 'assets' / 'sounds' / 'disparo.mp3'
)
enemy_hit_sound = mixer.Sound(
    Path(__file__).parent / 'assets' / 'sounds' / 'Golpe.mp3'
)

# Player var
player_img = pygame.image.load(Path(__file__).parent / 'assets' / 'img' / 'ship.png')
player_img = pygame.transform.scale(player_img, (64, 32))
player_x = 368
player_y = 500
player_x_change = 0
speed_multiplier = 2.5
player_speed = 0.6 * speed_multiplier

# Enemy var
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_amount = 8
enemy_spawn_limit = 20
enemies_spawned = 0

for e in range(enemy_amount):
    image = pygame.image.load(
        Path(__file__).parent / 'assets' / 'img' / 'ufo1.png'
    )
    scaled_image = pygame.transform.scale(image, (64, 64))
    enemy_img.append(scaled_image)
    enemy_x.append(
        random.randint(0, screen.get_width() - scaled_image.get_width())
    )
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.5 * speed_multiplier)
    enemy_y_change.append(50 * speed_multiplier)
    enemies_spawned += 1
enemies_killed_since_spawn = 0


# Shoot var
shoot_img = pygame.image.load(Path(__file__).parent / 'assets' / 'img' / 'shoot.png')
shoot_img = pygame.transform.scale(shoot_img, (24, 32))
shoot_x = 0
shoot_y = 500
shoot_x_change = 0
shoot_y_change = 2.5 * speed_multiplier
shoot_visibility = False

# Score var
score = 0
main_font = pygame.font.Font(None, 32)
game_over_font_size = 180
while sum(
    pygame.font.Font(None, game_over_font_size).size(letter)[0]
    for letter in "Game Over"
) > screen.get_width() * 0.9:
    game_over_font_size -= 1
game_over_font = pygame.font.Font(None, game_over_font_size)
final_score_font = pygame.font.Font(None, 56)
text_x = 10
text_y = 10
game_over = False
game_result = ""

# Show score function
def show_score(x, y):
    text = main_font.render(str(score), True, (222, 226, 184))
    screen.blit(text, (x, y))

# Player creator
def player(x, y):
    screen.blit(player_img, (x, y))

# Enemy creator
def enemy(x, y, index):
    screen.blit(enemy_img[index], (x, y))

# Shoot creator
def shoot(x, y):
    screen.blit(shoot_img, (x, y))

# collisions detector
def collision(x_1, x_2, y_1, y_2, enemy_index):
    enemy_rect = pygame.Rect(
        x_1, y_1,
        enemy_img[enemy_index].get_width(),
        enemy_img[enemy_index].get_height()
    )
    shoot_rect = pygame.Rect(
        x_2, y_2, shoot_img.get_width(), shoot_img.get_height()
    )
    return enemy_rect.colliderect(shoot_rect)

def show_game_over(title):
    screen.fill((0, 0, 0))
    letters = []
    for index, letter in enumerate(title):
        color_factor = index / (len(title) - 1)
        color = tuple(
            round(start_color * (1 - color_factor))
            for start_color in (116, 17, 36)
        )
        letters.append(game_over_font.render(letter, True, color))

    title_width = sum(letter.get_width() for letter in letters)
    x = (screen.get_width() - title_width) // 2
    title_y = screen.get_height() // 2 - game_over_font.get_height()
    for letter in letters:
        screen.blit(letter, (x, title_y))
        x += letter.get_width()

    score_text = final_score_font.render(
        f"Score: {score}", True, (222, 226, 184)
    )
    score_rect = score_text.get_rect(
        center=(screen.get_width() // 2, title_y + game_over_font.get_height() + 50)
    )
    screen.blit(score_text, score_rect)

# Game's loop
playing = True
clock = pygame.time.Clock()
while playing:

    # Fondo
    screen.blit(fondo, (0, 0))

    # events iter
    for events in pygame.event.get():

        # close event
        if events.type == pygame.QUIT:
            playing = False

        # push keys
        if events.type == pygame.KEYDOWN and not game_over:
            if events.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if events.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if events.key == pygame.K_SPACE and not shoot_visibility:
                shoot_sound.play()
                shoot_x = player_x + (player_img.get_width() - shoot_img.get_width()) // 2
                shoot_y = player_y - shoot_img.get_height()
                shoot_visibility = True

        if events.type == pygame.KEYUP:
            if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                player_x_change = 0

    if game_over:
        show_game_over(game_result)
        pygame.display.update()
        clock.tick(60)
        continue

    # modifying player location
    player_x += player_x_change

    # maintain in borders
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # modifying enemy location
    for e in range(len(enemy_x)):
        enemy_x[e] += enemy_x_change[e]

        # maintain enemy in borders
        enemy_max_x = screen.get_width() - enemy_img[e].get_width()
        if enemy_x[e] <= 0 or enemy_x[e] >= enemy_max_x:
            enemy_x[e] = max(0, min(enemy_x[e], enemy_max_x))
            enemy_x_change[e] *= -1
            enemy_y[e] += enemy_y_change[e]

        player_rect = pygame.Rect(
            player_x, player_y, player_img.get_width(), player_img.get_height()
        )
        enemy_rect = pygame.Rect(
            enemy_x[e],
            enemy_y[e],
            enemy_img[e].get_width(),
            enemy_img[e].get_height(),
        )
        if player_rect.colliderect(enemy_rect):
            game_over = True
            game_result = "Game Over"
            break

    # Shoot movement
    if not game_over and shoot_visibility:
        shoot_y -= shoot_y_change
        if shoot_y <= -shoot_img.get_height():
            shoot_visibility = False

    # collision
    if not game_over and shoot_visibility:
        for e in range(len(enemy_x)):
            if collision(enemy_x[e], shoot_x, enemy_y[e], shoot_y, e):
                enemy_hit_sound.play()
                for enemy_list in (
                    enemy_img,
                    enemy_x,
                    enemy_y,
                    enemy_x_change,
                    enemy_y_change,
                ):
                    enemy_list.pop(e)
                shoot_visibility = False
                score += 1
                enemies_killed_since_spawn += 1
                if not enemy_x and enemies_spawned == enemy_spawn_limit:
                    game_over = True
                    game_result = "You Won!"
                elif (
                    enemies_killed_since_spawn == 2
                    and enemies_spawned < enemy_spawn_limit
                ):
                    enemy_img.append(enemy_img[0])
                    enemy_x.append(
                        random.randint(
                            0, screen.get_width() - enemy_img[0].get_width()
                        )
                    )
                    enemy_y.append(random.randint(50, 200))
                    enemy_x_change.append(0.5 * speed_multiplier)
                    enemy_y_change.append(50 * speed_multiplier)
                    enemies_spawned += 1
                    enemies_killed_since_spawn = 0
                break

    if shoot_visibility:
        shoot(shoot_x, shoot_y)

    player(player_x, player_y)
    for e in range(len(enemy_x)):
        enemy(enemy_x[e], enemy_y[e], e)

    show_score(text_x, text_y)
    if game_over:
        show_game_over(game_result)

    # Update game state
    pygame.display.update()
    clock.tick(60)
