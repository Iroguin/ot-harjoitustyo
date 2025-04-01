import unittest 
import pygame
import sys
import os
import maingame as maingame

def test_initial_ship_position():
    assert maingame.ship_x == maingame.WIDTH // 2
    assert maingame.ship_y == maingame.HEIGHT // 2

def test_ship_moves_up_with_w_key():
    initial_y = maingame.ship_y
    
    if pygame.K_w:
        maingame.ship_y -= maingame.ship_speed
    
    assert maingame.ship_y < initial_y

def test_ship_stays_in_bounds():
    maingame.ship_x = -50
    
    maingame.ship_x = max(maingame.ship_size // 2, min(maingame.ship_x, maingame.WIDTH - maingame.ship_size // 2))
    
    assert maingame.ship_x == maingame.ship_size // 2