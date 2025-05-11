"""Testing for the Asteroid class in the asteroid.py module."""
import unittest
from asteroid import Asteroid


class TestAsteroid(unittest.TestCase):
    def test_asteroid_creation(self):
        asteroid = Asteroid(800, 600)
        self.assertIsNotNone(asteroid.x)
        self.assertIsNotNone(asteroid.y)
        self.assertTrue(15 <= asteroid.size <= 40)

    def test_asteroid_movement(self):
        asteroid = Asteroid(800, 600)
        initial_x = asteroid.x
        initial_y = asteroid.y
        initial_velocity_x = asteroid.velocity_x
        initial_velocity_y = asteroid.velocity_y
        asteroid.update()
        self.assertAlmostEqual(initial_x + initial_velocity_x, asteroid.x)
        self.assertAlmostEqual(initial_y + initial_velocity_y, asteroid.y)

    def test_asteroid_removal_when_offscreen(self):
        asteroid = Asteroid(800, 600)
        asteroid.x = -100 - asteroid.size
        asteroid.y = 300
        asteroid.velocity_x = 0
        asteroid.velocity_y = 0
        asteroid.points = [(-100 - asteroid.size, 300)
                           for _ in range(len(asteroid.points))]
        self.assertFalse(asteroid.update())


if __name__ == "__main__":
    unittest.main()
