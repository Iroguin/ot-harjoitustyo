"""Module for asteroid objects in the game."""
import math
import random
import pygame


class Asteroid:
    """Class representing asteroid."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = random.randint(15, 40)
        self.spawn_side = random.choice(['top', 'right', 'bottom', 'left'])

        if self.spawn_side == 'top':
            self.x = random.randint(0, width)
            self.y = -self.size
        elif self.spawn_side == 'right':
            self.x = width + self.size
            self.y = random.randint(0, height)
        elif self.spawn_side == 'bottom':
            self.x = random.randint(0, width)
            self.y = height + self.size
        else:  # left
            self.x = -self.size
            self.y = random.randint(0, height)

        self.speed = random.uniform(1, 3)

        self.angle = random.uniform(0, 2 * math.pi)
        self.velocity_x = math.cos(self.angle) * self.speed
        self.velocity_y = math.sin(self.angle) * self.speed

        self.points = []
        num_points = random.randint(6, 10)
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            distance = random.uniform(0.8, 1.2) * self.size
            point_x = self.x + math.cos(angle) * distance
            point_y = self.y + math.sin(angle) * distance
            self.points.append((point_x, point_y))
        self.color = (180, 180, 180)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        for i, point in enumerate(self.points):
            self.points[i] = (point[0] + self.velocity_x,
                              point[1] + self.velocity_y)

        if (self.x + self.size < 0 or
            self.x - self.size > self.width or
            self.y + self.size < 0 or
                self.y - self.size > self.height):
            return False
        return True

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)

    def get_position(self):
        return (self.x, self.y)

    def get_size(self):
        return self.size