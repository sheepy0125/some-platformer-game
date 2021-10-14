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

        self.default_pos = list(default_pos)
        self.velocity_cap = (20, 10)
        self.vx = self.vy = 0

        self.land_time = 0

        self.scroll_x = self.scroll_y = 0

        self.collision_types = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
        }
        self.prev_on_ground = False

        self.create()

    def __str__(self):
        return f"{self.size=} {self.image_path=} {self.movement_speed=}"

    def create(self):
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.fall_surf = pygame.transform.scale(
            self.surface, (self.size[0] - 6, self.size[1] + 6)
        )
        self.land_surf = pygame.transform.scale(
            self.surface, (self.size[0] + 10, self.size[1] - 10)
        )
        self.rect = self.surface.get_rect(center=self.default_pos)

    def get_tile_collisions(self, tile_rects: list):
        return [
            tile_rect for tile_rect in tile_rects if self.rect.colliderect(tile_rect)
        ]

    def move(self, all_tiles: World):

        self.land_time += 1

        # Horizontal
        self.collision_types = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
        }

        # Add velocity
        if abs(self.vx > self.velocity_cap[0]):
            self.vx = self.velocity_cap[0]

        # Terminal velocity
        # if abs(self.vy) < self.velocity_cap[1]:
        # self.vy = self.velocity_cap[1]

        # Set position
        self.rect.x += self.vx

        # Check horizontal collision
        collision_list = self.get_tile_collisions(
            [tile.rect for tile in all_tiles.tile_map]
        )
        for tile in collision_list:
            # Moving right
            if self.vx > 0:
                self.rect.right = tile.left
                self.collision_types["right"] = True

            # Moving left
            elif self.vx < 0:
                self.rect.left = tile.right
                self.collision_types["left"] = True

            else:
                break

            # Collided, reset the velocity
            self.vx = 0

        # Vertical

        # Add velocity
        self.vy += GRAVITY
        self.rect.y += self.vy

        # Check vertical collision
        collision_list = self.get_tile_collisions(
            [tile.rect for tile in all_tiles.tile_map]
        )
        for tile in collision_list:
            # Moving up
            if self.vy < 0:
                self.rect.top = tile.bottom
                self.collision_types["top"] = True

            # Moving down
            elif self.vy > 0:
                self.rect.bottom = tile.top
                self.collision_types["bottom"] = True
                if not self.prev_on_ground:
                    self.land_time = 0

            else:
                break


            # Collided, reset the velocity
            self.vy = 0

        self.prev_on_ground = self.collision_types["bottom"]
        

    def draw(self, scroll_x, scroll_y):
        surface = self.surface
        draw_x = self.rect.x
        draw_y = self.rect.y
        if self.vy > 0:
            surface = self.fall_surf
            draw_x += 3
            draw_y -= 3

        elif self.land_time < 6:
            surface = self.land_surf
            draw_x -= 5
            draw_y += 10
        screen.blit(
            surface,
            (draw_x - scroll_x, draw_y - scroll_y),
        )


##############
### Player ###
##############
class Player(Entity):
    def __init__(self):
        super().__init__(
            size=(30, 50),
            image_path=str(ROOT_PATH / "assets" / "images" / "player.png"),
            default_pos=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
        )

        self.air_time = 0
        self.air_time_grace_period = 5

        Logger.log("Created player")

    def event_handler(self):
        keys: dict = pygame.key.get_pressed()

        # Air time check (allowed to jump a bit after losing contact with ground)
        if self.collision_types["bottom"]:
            self.air_time = 0
        else:
            self.air_time += 1

        # Jump
        if keys[pygame.K_UP]:
            # Possible to jump
            if (
                self.collision_types["bottom"]
                or self.air_time < self.air_time_grace_period
            ):
                self.vy = -20

        # Right
        if keys[pygame.K_RIGHT]:
            self.vx = 10

        # Left
        elif keys[pygame.K_LEFT]:
            self.vx = -10

        # None
        else:
            self.vx = 0

        # Other keys

        # Reset
        if keys[pygame.K_r]:
            self.vx = self.vy = 0
            self.rect.center = self.default_pos
