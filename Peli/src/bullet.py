"""Module for bullet objects in the game."""
import math
import random
import pygame

WHITE = (255, 255, 255)


class Bullet:
    """Class representing players bullets."""

    def __init__(self, x, y, angle, width, height, speed=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = 2
        self.speed = speed

        angle_with_spread = angle + random.uniform(-5, 5)
        angle_rad = math.radians(angle_with_spread)

        self.velocity_x = math.sin(angle_rad) * self.speed
        self.velocity_y = -math.cos(angle_rad) * self.speed

        self.color = WHITE

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # check if bullet is off screen
        if (self.x + self.size < 0 or
            self.x - self.size > self.width or
            self.y + self.size < 0 or
                self.y - self.size > self.height):
            return False
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)), self.size)

    def get_position(self):
        return (self.x, self.y)

    def get_size(self):
        return self.size
