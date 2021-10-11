"""
Pygame setup for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

import pygame
from config_parser import *

SCREEN_SIZE = (500, 500)
MAP_HEIGHT = 20
TILE_SIZE = round(SCREEN_SIZE[1] / MAP_HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Some Platformer Game")
clock = pygame.time.Clock()
