# pylint: disable=no-member
"""Main game module."""
import sys
import math
import pygame
from asteroid import Asteroid

pygame.init()

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

ASTEROIDS = []
ASTEROID_SPAWN_TIMER = 0
ASTEROID_SPAWN_INTERVAL = 60


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


def main():
    """Main game loop."""
    global SHIP_X, SHIP_Y, SHIP_ANGLE, ASTEROID_SPAWN_TIMER, ASTEROID_SPAWN_INTERVAL, ASTEROIDS
    global SHIP_VELOCITY_X, SHIP_VELOCITY_Y
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        delta_x = mouse_x - SHIP_X
        delta_y = mouse_y - SHIP_Y

        SHIP_ANGLE = math.degrees(math.atan2(delta_x, -delta_y))

        # Controls
        keys = pygame.key.get_pressed()
        SHIP_ANGLE %= 360

        if keys[pygame.K_w]:
            SHIP_VELOCITY_X += math.sin(math.radians(SHIP_ANGLE)) * SHIP_THRUST
            SHIP_VELOCITY_Y -= math.cos(math.radians(SHIP_ANGLE)) * SHIP_THRUST
        if keys[pygame.K_s]:
            SHIP_VELOCITY_X -= math.sin(math.radians(SHIP_ANGLE)) * SHIP_THRUST / 2
            SHIP_VELOCITY_Y += math.cos(math.radians(SHIP_ANGLE)) * SHIP_THRUST / 2
        if keys[pygame.K_a]:
            SHIP_VELOCITY_X -= math.cos(math.radians(SHIP_ANGLE)) * SHIP_THRUST / 2
            SHIP_VELOCITY_Y -= math.sin(math.radians(SHIP_ANGLE)) * SHIP_THRUST / 2
        if keys[pygame.K_d]:
            SHIP_VELOCITY_X += math.cos(math.radians(SHIP_ANGLE)) * SHIP_THRUST / 2
            SHIP_VELOCITY_Y += math.sin(math.radians(SHIP_ANGLE)) * SHIP_THRUST / 2

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

        # Asteroids
        ASTEROID_SPAWN_TIMER += 1
        if ASTEROID_SPAWN_TIMER >= ASTEROID_SPAWN_INTERVAL:
            ASTEROIDS.append(Asteroid(WIDTH, HEIGHT))
            ASTEROID_SPAWN_TIMER = 0
            ASTEROID_SPAWN_INTERVAL = max(20, ASTEROID_SPAWN_INTERVAL - 0.5)

        updated_asteroids = []
        for asteroid in ASTEROIDS:
            if asteroid.update():
                updated_asteroids.append(asteroid)
        ASTEROIDS = updated_asteroids
        screen.fill(BLACK)
        for asteroid in ASTEROIDS:
            asteroid.draw(screen)
        draw_ship(SHIP_X, SHIP_Y, SHIP_ANGLE)

        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Asteroids: {len(ASTEROIDS)}", True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
