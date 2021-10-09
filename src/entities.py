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
        self.velocity = [0, 0]
        self.velocity_cap = (20, 10)
        self.movement_multiplier = 0

        self.create()

    def __str__(self):
        return f"{self.size=} {self.image_path=} {self.movement_speed=}"

    def create(self):
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.rect = self.surface.get_rect(center=self.pos)

    def move(self):
        # Add velocity
        self.velocity[0] += 5 * self.movement_multiplier
        if abs(self.velocity[0] > self.velocity_cap[0]):
            self.velocity[0] = self.velocity_cap[0]

        # Terminal velocity
        if abs(self.velocity[0]) > self.velocity_cap[0]:
            self.velocity[0] = self.velocity_cap[0] * self.movement_multiplier

        if self.movement_multiplier == 0:
            self.velocity[0] = 0

        new_pos = [self.rect.centerx + self.velocity[0], self.pos[1]]

        self.set_pos(new_pos)

    def set_pos(self, new_pos: tuple):
        self.rect.centerx, self.rect.centery = new_pos
        self.pos = list(new_pos)

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
        keys: dict = pygame.key.get_pressed()

        self.jump_gravity_handler(jump_pressed=keys[pygame.K_UP])

        # Right
        if keys[pygame.K_RIGHT]:
            self.movement_multiplier = 1

        # Left
        elif keys[pygame.K_LEFT]:
            self.movement_multiplier = -1

        # None
        else:
            self.movement_multiplier = 0

    def jump_gravity_handler(self, jump_pressed: bool):
        # Gravity! (falling)
        self.velocity[1] += GRAVITY_MULTIPLIER

        if jump_pressed:
            self.velocity[1] = -5 * (GRAVITY_MULTIPLIER * 2)

        self.pos[1] += self.velocity[1]
