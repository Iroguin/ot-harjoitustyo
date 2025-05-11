"""Asteroid class for the game."""
import math
import random
import pygame


class Asteroid:
    """Class representing an asteroid in the game."""

    def __init__(self, width, height):
        self.bounds = (width, height)
        self.size = random.randint(15, 40)
        self.x, self.y = self._spawn_position()
        self.velocity_x, self.velocity_y = self._init_velocity()
        self.points = self._generate_points()
        self.color = (180, 180, 180)

    def _spawn_position(self):
        width, height = self.bounds
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            return random.randint(0, width), -self.size
        if side == 'right':
            return width + self.size, random.randint(0, height)
        if side == 'bottom':
            return random.randint(0, width), height + self.size
        # left
        return -self.size, random.randint(0, height)

    def _init_velocity(self):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        return math.cos(angle) * speed, math.sin(angle) * speed

    def _generate_points(self):
        num_points = random.randint(6, 10)
        points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            distance = random.uniform(0.8, 1.2) * self.size
            px = self.x + math.cos(angle) * distance
            py = self.y + math.sin(angle) * distance
            points.append((px, py))
        return points

    def update(self):
        bx, by = self.bounds
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.points = [(px + self.velocity_x, py + self.velocity_y)
                       for px, py in self.points]

        off_left = self.x + self.size < 0
        off_right = self.x - self.size > bx
        off_top = self.y + self.size < 0
        off_bottom = self.y - self.size > by
        return not (off_left or off_right or off_top or off_bottom)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)

    def get_position(self):
        return self.x, self.y

    def get_size(self):
        return self.size
