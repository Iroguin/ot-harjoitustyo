"""Main game module."""
import sys
import math
import pygame
from asteroid import Asteroid
from bullet import Bullet
from game_ui import GameUI, STATE_GAME, STATE_PAUSED

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Spaceship Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SHIP_SIZE = 30
SHIP_X = WIDTH // 2
SHIP_Y = HEIGHT // 2
SHIP_VELOCITY_X = 0
SHIP_VELOCITY_Y = 0
SHIP_THRUST = 0.2
SHIP_MAX_SPEED = 8
SHIP_FRICTION = 0.98  # 1 = no friction
SHIP_ANGLE = 0
SHIP_HEALTH = 100

BULLETS = []
BULLET_COOLDOWN = 10
BULLET_TIMER = 0

ASTEROIDS = []
ASTEROID_SPAWN_TIMER = 0
ASTEROID_SPAWN_INTERVAL = 60

SCORE = 0


def draw_ship(x, y, angle):
    """Draw the spaceship at the given position and angle."""
    angle_rad = math.radians(angle)
    nose = (0, -SHIP_SIZE // 2)
    left_wing = (-SHIP_SIZE // 2, SHIP_SIZE // 2)
    right_wing = (SHIP_SIZE // 2, SHIP_SIZE // 2)

    def rotate(point):
        px, py = point
        rx = px * math.cos(angle_rad) - py * math.sin(angle_rad)
        ry = px * math.sin(angle_rad) + py * math.cos(angle_rad)
        return (rx + x, ry + y)

    rotated_nose = rotate(nose)
    rotated_left_wing = rotate(left_wing)
    rotated_right_wing = rotate(right_wing)
    pygame.draw.polygon(
        screen, WHITE, [rotated_nose, rotated_left_wing, rotated_right_wing])


def reset_game():
    """Reset to initial state."""
    global SHIP_X, SHIP_Y, SHIP_VELOCITY_X, SHIP_VELOCITY_Y, SHIP_ANGLE, SHIP_HEALTH
    global BULLETS, ASTEROIDS, ASTEROID_SPAWN_TIMER, ASTEROID_SPAWN_INTERVAL, SCORE

    SHIP_X = WIDTH // 2
    SHIP_Y = HEIGHT // 2
    SHIP_VELOCITY_X = 0
    SHIP_VELOCITY_Y = 0
    SHIP_ANGLE = 0
    SHIP_HEALTH = 100

    BULLETS = []
    ASTEROIDS = []
    ASTEROID_SPAWN_TIMER = 0
    ASTEROID_SPAWN_INTERVAL = 60
    SCORE = 0


def main():
    """Main game loop."""
    global SHIP_X, SHIP_Y, SHIP_ANGLE, SHIP_HEALTH, SHIP_VELOCITY_X, SHIP_VELOCITY_Y
    global ASTEROID_SPAWN_TIMER, ASTEROID_SPAWN_INTERVAL, ASTEROIDS, BULLET_TIMER, SCORE, BULLETS
    clock = pygame.time.Clock()
    ui = GameUI(WIDTH, HEIGHT)
    game_state = ui.state
    running = True

    while running:
        mouse_clicked = False
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        prev_state = game_state
        game_state, action = ui.update(mouse_pos, mouse_clicked, keys)

        if action == 'quit':
            running = False
        elif action in ('start', 'restart', 'main_menu'):
            reset_game()

        if game_state == STATE_GAME:
            if prev_state == STATE_PAUSED:
                mouse_clicked = False

            if BULLET_TIMER > 0:
                BULLET_TIMER -= 1

            delta_x = mouse_pos[0] - SHIP_X
            delta_y = mouse_pos[1] - SHIP_Y

            SHIP_ANGLE = math.degrees(math.atan2(delta_x, -delta_y))

            keys = pygame.key.get_pressed()
            SHIP_ANGLE %= 360

            if keys[pygame.K_w]:
                SHIP_VELOCITY_X += math.sin(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST
                SHIP_VELOCITY_Y -= math.cos(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST
            if keys[pygame.K_s]:
                SHIP_VELOCITY_X -= math.sin(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST / 2
                SHIP_VELOCITY_Y += math.cos(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST / 2
            if keys[pygame.K_a]:
                SHIP_VELOCITY_X -= math.cos(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST / 2
                SHIP_VELOCITY_Y -= math.sin(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST / 2
            if keys[pygame.K_d]:
                SHIP_VELOCITY_X += math.cos(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST / 2
                SHIP_VELOCITY_Y += math.sin(math.radians(SHIP_ANGLE)
                                            ) * SHIP_THRUST / 2

            if (keys[pygame.K_SPACE] or mouse_clicked) and BULLET_TIMER == 0:
                position = (SHIP_X, SHIP_Y)
                BULLETS.append(
                    Bullet(position, SHIP_ANGLE, (WIDTH, HEIGHT)))
                BULLET_TIMER = BULLET_COOLDOWN

            SHIP_VELOCITY_X *= SHIP_FRICTION
            SHIP_VELOCITY_Y *= SHIP_FRICTION

            speed = math.sqrt(SHIP_VELOCITY_X**2 + SHIP_VELOCITY_Y**2)
            if speed > SHIP_MAX_SPEED:
                SHIP_VELOCITY_X = SHIP_VELOCITY_X / speed * SHIP_MAX_SPEED
                SHIP_VELOCITY_Y = SHIP_VELOCITY_Y / speed * SHIP_MAX_SPEED

            SHIP_X += SHIP_VELOCITY_X
            SHIP_Y += SHIP_VELOCITY_Y

            SHIP_X = max(SHIP_SIZE // 2, min(SHIP_X, WIDTH - SHIP_SIZE // 2))
            SHIP_Y = max(SHIP_SIZE // 2, min(SHIP_Y, HEIGHT - SHIP_SIZE // 2))

            updated_bullets = []
            for bullet in BULLETS:
                if bullet.update():
                    updated_bullets.append(bullet)
            BULLETS = updated_bullets

            ASTEROID_SPAWN_TIMER += 1
            if ASTEROID_SPAWN_TIMER >= ASTEROID_SPAWN_INTERVAL:
                ASTEROIDS.append(Asteroid(WIDTH, HEIGHT))
                ASTEROID_SPAWN_TIMER = 0
                ASTEROID_SPAWN_INTERVAL = max(
                    20, ASTEROID_SPAWN_INTERVAL - 0.5)

            updated_asteroids = []
            for asteroid in ASTEROIDS:
                if asteroid.update():
                    updated_asteroids.append(asteroid)

                    asteroid_pos = asteroid.get_position()
                    asteroid_size = asteroid.get_size()
                    distance = math.sqrt(
                        (asteroid_pos[0] - SHIP_X)**2 + (asteroid_pos[1] - SHIP_Y)**2)

                    if distance < asteroid_size + SHIP_SIZE // 2:
                        SHIP_HEALTH -= 10

                    for bullet in BULLETS:
                        bullet_pos = bullet.get_position()
                        bullet_size = bullet.get_size()
                        bullet_distance = math.sqrt((asteroid_pos[0] - bullet_pos[0])**2 +
                                                    (asteroid_pos[1] - bullet_pos[1])**2)

                        if bullet_distance < asteroid_size + bullet_size:
                            if bullet in BULLETS:
                                BULLETS.remove(bullet)
                            if asteroid in updated_asteroids:
                                updated_asteroids.remove(asteroid)
                                SCORE += 10
                            break

            ASTEROIDS = updated_asteroids
            ui.set_player_health(SHIP_HEALTH)
            ui.set_score(SCORE)
            if SHIP_HEALTH <= 0:
                ui.game_over()
        screen.fill(BLACK)

        if game_state in (STATE_GAME, STATE_PAUSED):
            for bullet in BULLETS:
                bullet.draw(screen)

            for asteroid in ASTEROIDS:
                asteroid.draw(screen)

            draw_ship(SHIP_X, SHIP_Y, SHIP_ANGLE)

        ui.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
