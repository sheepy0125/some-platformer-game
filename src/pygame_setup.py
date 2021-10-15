"""
Pygame setup for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

import pygame
from config_parser import FPS, GRAVITY, SCROLL_OFFSET

SCREEN_SIZE = (500, 500)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Some Platformer Game")
clock = pygame.time.Clock()
