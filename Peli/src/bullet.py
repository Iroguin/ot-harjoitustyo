"""Bullet class for the game."""
import math
import random
import pygame

WHITE = (255, 255, 255)


class Bullet:
    """Class representing player bullets."""

    def __init__(self, position, angle, bounds, speed=10):
        self.x, self.y = position
        self.bounds = bounds
        self.size = 2
        self.speed = speed

        angle_with_spread = angle + random.uniform(-5, 5)
        self.velocity_x, self.velocity_y = self._init_velocity(
            angle_with_spread)

        self.color = WHITE

    def _init_velocity(self, angle_deg):
        angle_rad = math.radians(angle_deg)
        vx = math.sin(angle_rad) * self.speed
        vy = -math.cos(angle_rad) * self.speed
        return vx, vy

    def update(self):
        width, height = self.bounds
        self.x += self.velocity_x
        self.y += self.velocity_y

        off_left = self.x + self.size < 0
        off_right = self.x - self.size > width
        off_top = self.y + self.size < 0
        off_bottom = self.y - self.size > height
        return not (off_left or off_right or off_top or off_bottom)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.size)

    def get_position(self):
        return self.x, self.y

    def get_size(self):
        return self.size
