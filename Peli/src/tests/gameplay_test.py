""""Testing the gameplay of the game."""
import unittest
import pygame
import math
import maingame
from unittest.mock import patch


class TestMainGame(unittest.TestCase):
    def setUp(self):
        maingame.reset_game()

    def test_initial_ship_position(self):
        self.assertEqual(maingame.SHIP_X, maingame.WIDTH // 2)
        self.assertEqual(maingame.SHIP_Y, maingame.HEIGHT // 2)
        self.assertEqual(maingame.SHIP_VELOCITY_X, 0)
        self.assertEqual(maingame.SHIP_VELOCITY_Y, 0)
        self.assertEqual(maingame.SHIP_ANGLE, 0)
        self.assertEqual(maingame.SHIP_HEALTH, 100)

    @patch('pygame.key.get_pressed')
    def test_ship_acceleration_with_w_key(self, mock_get_pressed):
        mock_keys = {pygame.K_w: True}
        mock_get_pressed.return_value = mock_keys
        maingame.SHIP_ANGLE = 0
        maingame.SHIP_VELOCITY_X = 0
        maingame.SHIP_VELOCITY_Y = 0

        if mock_keys[pygame.K_w]:
            maingame.SHIP_VELOCITY_X += math.sin(math.radians(
                maingame.SHIP_ANGLE)) * maingame.SHIP_THRUST
            maingame.SHIP_VELOCITY_Y -= math.cos(math.radians(
                maingame.SHIP_ANGLE)) * maingame.SHIP_THRUST

        self.assertEqual(maingame.SHIP_VELOCITY_X, 0)
        self.assertLess(maingame.SHIP_VELOCITY_Y, 0)

    def test_ship_stays_in_bounds(self):
        maingame.SHIP_X = -50
        maingame.SHIP_X = max(maingame.SHIP_SIZE // 2,
                              min(maingame.SHIP_X, maingame.WIDTH - maingame.SHIP_SIZE // 2))
        self.assertEqual(maingame.SHIP_X, maingame.SHIP_SIZE // 2)

        maingame.SHIP_X = maingame.WIDTH + 50
        maingame.SHIP_X = max(maingame.SHIP_SIZE // 2,
                              min(maingame.SHIP_X, maingame.WIDTH - maingame.SHIP_SIZE // 2))
        self.assertEqual(maingame.SHIP_X, maingame.WIDTH -
                         maingame.SHIP_SIZE // 2)

        maingame.SHIP_Y = -50
        maingame.SHIP_Y = max(maingame.SHIP_SIZE // 2,
                              min(maingame.SHIP_Y, maingame.HEIGHT - maingame.SHIP_SIZE // 2))
        self.assertEqual(maingame.SHIP_Y, maingame.SHIP_SIZE // 2)

        maingame.SHIP_Y = maingame.HEIGHT + 50
        maingame.SHIP_Y = max(maingame.SHIP_SIZE // 2,
                              min(maingame.SHIP_Y, maingame.HEIGHT - maingame.SHIP_SIZE // 2))
        self.assertEqual(maingame.SHIP_Y, maingame.HEIGHT -
                         maingame.SHIP_SIZE // 2)

    def test_reset_game(self):
        maingame.SHIP_X = 100
        maingame.SHIP_Y = 100
        maingame.SHIP_VELOCITY_X = 5
        maingame.SHIP_VELOCITY_Y = 5
        maingame.SHIP_ANGLE = 45
        maingame.SHIP_HEALTH = 50
        maingame.BULLETS.append("dummy bullet")
        maingame.ASTEROIDS.append("dummy asteroid")
        maingame.SCORE = 100

        maingame.reset_game()

        self.assertEqual(maingame.SHIP_X, maingame.WIDTH // 2)
        self.assertEqual(maingame.SHIP_Y, maingame.HEIGHT // 2)
        self.assertEqual(maingame.SHIP_VELOCITY_X, 0)
        self.assertEqual(maingame.SHIP_VELOCITY_Y, 0)
        self.assertEqual(maingame.SHIP_ANGLE, 0)
        self.assertEqual(maingame.SHIP_HEALTH, 100)
        self.assertEqual(len(maingame.BULLETS), 0)
        self.assertEqual(len(maingame.ASTEROIDS), 0)
        self.assertEqual(maingame.SCORE, 0)

    def test_speed_limiting(self):
        maingame.SHIP_VELOCITY_X = 20
        maingame.SHIP_VELOCITY_Y = 0
        speed = math.sqrt(maingame.SHIP_VELOCITY_X**2 +
                          maingame.SHIP_VELOCITY_Y**2)
        if speed > maingame.SHIP_MAX_SPEED:
            maingame.SHIP_VELOCITY_X = maingame.SHIP_VELOCITY_X / \
                speed * maingame.SHIP_MAX_SPEED
            maingame.SHIP_VELOCITY_Y = maingame.SHIP_VELOCITY_Y / \
                speed * maingame.SHIP_MAX_SPEED

        self.assertEqual(maingame.SHIP_VELOCITY_X, maingame.SHIP_MAX_SPEED)
        self.assertEqual(maingame.SHIP_VELOCITY_Y, 0)


if __name__ == "__main__":
    unittest.main()
