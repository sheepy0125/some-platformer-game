"""
Pygame setup for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

import pygame

SCREEN_SIZE = (500, 500)
SCROLL_OFFSET = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Some Platformer Game")
clock = pygame.time.Clock()
