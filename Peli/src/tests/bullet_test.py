"""Testing for the Bullet class in the bullet.py module."""
import unittest
from bullet import Bullet


class TestBullet(unittest.TestCase):
    def test_bullet_initialization(self):
        bullet = Bullet((100, 200), 45, (800, 600))
        self.assertEqual(bullet.x, 100)
        self.assertEqual(bullet.y, 200)
        self.assertEqual(bullet.size, 2)
        self.assertIsNotNone(bullet.velocity_x)
        self.assertIsNotNone(bullet.velocity_y)

    def test_bullet_movement(self):
        bullet = Bullet((100, 100), 90, (800, 600))
        initial_x = bullet.x
        initial_y = bullet.y
        initial_velocity_x = bullet.velocity_x
        initial_velocity_y = bullet.velocity_y
        bullet.update()
        self.assertAlmostEqual(initial_x + initial_velocity_x, bullet.x)
        self.assertAlmostEqual(initial_y + initial_velocity_y, bullet.y)

    def test_bullet_removal_when_offscreen(self):
        bullet = Bullet((100, 100), 0, (800, 600))
        bullet.x = 100
        bullet.y = -10
        bullet.velocity_x = 0
        bullet.velocity_y = -5
        self.assertFalse(bullet.update())

    def test_bullet_stays_onscreen(self):
        bullet = Bullet((400, 300), 45, (800, 600))
        bullet.x = 400
        bullet.y = 300
        self.assertTrue(bullet.update())


if __name__ == "__main__":
    unittest.main()
