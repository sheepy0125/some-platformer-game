"""
Entities for Some Platformer Game
Created by duuuck and sheepy0125
08/10/2021
"""

import pygame
from pygame_setup import *
from config_parser import *
from world import World
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

    def set_pos(self, new_pos: list | tuple):
        self.rect.centerx, self.rect.centery = new_pos

    def get_tile_collisions(self, tile_rects: list):
        return [
            tile_rect for tile_rect in tile_rects if self.rect.colliderect(tile_rect)
        ]

    def move(self, all_tiles: World):
        self.collision_types = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
        }

        # Horizontal

        # Add velocity
        self.velocity[0] += 10 * self.movement_multiplier
        if abs(self.velocity[0] > self.velocity_cap[0]):
            self.velocity[0] = self.velocity_cap[0]

        if self.movement_multiplier == 0:
            self.velocity[0] = 0

        # Terminal velocity
        if abs(self.velocity[0]) > self.velocity_cap[0]:
            self.velocity[0] = self.velocity_cap[0] * self.movement_multiplier

        # Set position
        new_pos = [self.rect.centerx + self.velocity[0], self.rect.centery]
        self.set_pos(new_pos)

        # Check horizontal collision
        collision_list = self.get_tile_collisions(
            [tile.rect for tile in all_tiles.tile_map]
        )
        for tile in collision_list:
            # Moving right
            if self.velocity[0] > 0:
                self.rect.right = tile.left
                self.collision_types["right"] = True

            # Moving left
            elif self.velocity[0] < 0:
                self.rect.left = tile.right
                self.collision_types["left"] = True

            else:
                break

            # Collided, reset the velocity
            self.velocity[0] = 0

        # Vertical

        # Add velocity
        self.velocity[1] += 1
        new_pos = [self.rect.centerx, self.rect.centery + self.velocity[1]]
        self.set_pos(new_pos)

        # Check vertical collision
        collision_list = self.get_tile_collisions(
            [tile.rect for tile in all_tiles.tile_map]
        )
        for tile in collision_list:
            # Moving up
            if self.velocity[1] < 0:
                self.rect.top = tile.bottom
                self.collision_types["top"] = True

            # Moving down
            elif self.velocity[1] > 0:
                self.rect.bottom = tile.top
                self.collision_types["bottom"] = True

            else:
                break

            # Collided, reset the velocity
            self.velocity[1] = 0

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

        # Jump
        if keys[pygame.K_UP]:
            # Possible to jump
            if self.collision_types["bottom"]:
                self.velocity[1] = -20 * GRAVITY_MULTIPLIER

        # Right
        if keys[pygame.K_RIGHT]:
            self.movement_multiplier = 1

        # Left
        elif keys[pygame.K_LEFT]:
            self.movement_multiplier = -1

        # None
        else:
            self.movement_multiplier = 0
