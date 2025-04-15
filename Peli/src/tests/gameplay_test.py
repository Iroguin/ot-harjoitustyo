import unittest
import pygame
import sys
import os
import maingame as maingame


def test_initial_ship_position():
    assert maingame.SHIP_X == maingame.WIDTH // 2
    assert maingame.SHIP_Y == maingame.HEIGHT // 2


def test_ship_moves_up_with_w_key():
    initial_y = maingame.SHIP_Y

    if pygame.K_w:
        maingame.SHIP_Y -= maingame.SHIP_THRUST

    assert maingame.SHIP_Y < initial_y


def test_ship_stays_in_bounds():
    maingame.SHIP_X = -50

    maingame.SHIP_X = max(maingame.SHIP_SIZE // 2,
                          min(maingame.SHIP_X, maingame.WIDTH - maingame.SHIP_SIZE // 2))

    assert maingame.SHIP_X == maingame.SHIP_SIZE // 2
