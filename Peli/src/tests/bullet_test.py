import unittest
from bullet import Bullet


class TestBullet(unittest.TestCase):
    def test_bullet_initialization(self):
        bullet = Bullet(100, 200, 45, 800, 600)
        self.assertEqual(bullet.x, 100)
        self.assertEqual(bullet.y, 200)
        self.assertEqual(bullet.size, 2)
        
    def test_bullet_movement(self):
        bullet = Bullet(100, 100, 90, 800, 600)
        initial_x = bullet.x
        bullet.update()
        self.assertGreater(bullet.x, initial_x)


if __name__ == "__main__":
    unittest.main()
