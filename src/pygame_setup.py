"""
Pygame setup for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

import pygame
from config_parser import *

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Some Platformer Game")
clock = pygame.time.Clock()