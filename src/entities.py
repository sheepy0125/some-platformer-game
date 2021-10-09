"""
Entities for Some Platformer Game
Created by duuuck and sheepy0125
08/10/2021
"""

import pygame
from pygame_setup import *
from config_parser import *
from utils import Logger, ROOT_PATH

##############
### Entity ###
##############
class Entity:
    """Base entity class"""

    def __init__(self, size: tuple, image_path: str, default_pos: list):
        self.size = size
        self.image_path = image_path
        self.pos = list(default_pos)
        self.vy = 0
        self.create()

    def __str__(self):
        return f"{self.size=} {self.image_path=} {self.movement_speed=}"

    def create(self):
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.rect = self.surface.get_rect(center=self.pos)

    def move(self, new_pos: tuple):
        self.rect.centerx, self.rect.centery = new_pos
        self.pos = new_pos

    def get_collisions(self, rects) -> list:
        return [other_rect for other_rect in rects if self.rect.colliderect(other_rect)]

    def draw(self):
        screen.blit(self.surface, (self.rect.left, self.rect.top))


##############
### Player ###
##############
class Player(Entity):
    def __init__(self):
        super().__init__(
            size=(50, 100),
            image_path=str(ROOT_PATH / "assets" / "images" / "player.png"),
            default_pos=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
        )

        Logger.log("Created player")

    def movement_handler(self):
        MOVE_BY = 10
        GRAVITY = 1
        keys: dict = pygame.key.get_pressed()
        self.vy += GRAVITY
        self.pos[1] += self.vy

        # Right
        if keys[pygame.K_RIGHT]:
            self.pos[0] += MOVE_BY
        # Left
        if keys[pygame.K_LEFT]:
            self.pos[0] -= MOVE_BY



        self.move(self.pos)
