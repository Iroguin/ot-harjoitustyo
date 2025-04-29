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
        asteroid.update()
        self.assertNotEqual((initial_x, initial_y), (asteroid.x, asteroid.y))
        
    def test_asteroid_removal_when_offscreen(self):
        asteroid = Asteroid(800, 600)
        asteroid.x = -100
        asteroid.y = -100
        for i in range(len(asteroid.points)):
            asteroid.points[i] = (-100, -100)
        self.assertFalse(asteroid.update())


if __name__ == "__main__":
    unittest.main()