"""
Entities for Some Platformer Game
Created by duuuck and sheepy0125
08/10/2021
"""

import pygame
from pygame_setup import *
from config_parser import *

##############
### Entity ###
##############
class Entity:
    """Base entity class"""

    def __init__(self, size: tuple, image_path: str, default_pos: tuple):
        self.size = size
        self.image_path = image_path
        self.pos = default_pos

        self.create()

    def __str__(self):
        return f"{self.size=} {self.image_path=} {self.movement_speed=}"

    def create(self):
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.rect = self.surface.get_rect(center=self.pos)

    def move(self, new_pos: tuple):
        self.rect.move(new_pos)

    def check_collision(self, other_rect) -> bool:
        return self.rect.colliderect(other_rect)

    def draw(self):
        screen.blit(self.surface, self.rect)


##############
### Player ###
##############
class Player(Entity):
    def __init__(self):
        super().__init__(
            size=(50, 100),
            image_path=f"assets/images/player.png",
            default_pos=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
        )

        Logger.log("Created player")
