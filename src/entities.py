"""
Entities for Some Platformer Game
Created by duuuuck and sheepy0125
08/10/2021
"""

from pygame_setup import pygame, screen, SCREEN_SIZE, SCROLL_OFFSET
from config_parser import FPS, GRAVITY
from utils import Logger, Scrolling, ROOT_PATH
from world import World

from time import time


##############
### Entity ###
##############
class Entity:
    """Base entity class"""

    def __init__(self, size: tuple, image_path: str, default_pos: tuple):
        self.size = size
        self.image_path = image_path
        self.default_pos = list(default_pos)
        self.velocity_cap = (20, 10)
        self.vx = self.vy = 0

        self.land_time = time()

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
        self.rect = self.surface.get_rect(center=self.default_pos)

    def get_tile_collisions(self, tile_rects: list):
        return [
            tile_rect for tile_rect in tile_rects if self.rect.colliderect(tile_rect)
        ]

    def move(self, world: World):

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
        self.rect.x += round(self.vx)

        # Check horizontal collision
        collision_list = self.get_tile_collisions(world.map_list)
        for tile in collision_list:
            # Moving right
            if self.vx > 0:
                self.rect.right = tile.rect.left
                self.collision_types["right"] = True

            # Moving left
            elif self.vx < 0:
                self.rect.left = tile.rect.right
                self.collision_types["left"] = True

            else:
                break

            # Collided, reset the velocity
            self.vx = 0

        # Vertical

        # Add velocity
        self.vy += GRAVITY * 1.5
        self.rect.y += self.vy

        # Check vertical collision
        collision_list = self.get_tile_collisions(world.map_list)
        for tile in collision_list:
            # Moving up
            if self.vy < 0:
                self.rect.top = tile.rect.bottom
                self.collision_types["top"] = True

            # Moving down
            elif self.vy > 0:
                self.rect.bottom = tile.rect.top
                self.collision_types["bottom"] = True
                if not self.prev_on_ground:
                    self.land_time = time()

            else:
                break

            # Collided, reset the velocity
            self.vy = 0

        self.prev_on_ground = self.collision_types["bottom"]

    def draw(self):
        # Squashing and stretching
        surface = self.surface
        draw_x = self.rect.x
        draw_y = self.rect.y

        # Stretching
        if not self.collision_types["bottom"]:
            surface = pygame.transform.scale(
                surface, (self.size[0] - 6, self.size[1] + 6)
            )
            draw_x += 3
            draw_y -= 3

        # Squashing
        elif time() - self.land_time < 0.1:
            surface = pygame.transform.scale(
                surface, (self.size[0] + 10, self.size[1] - 10)
            )
            draw_x -= 5
            draw_y += 10

        # Draw
        screen.blit(
            surface,
            (draw_x - Scrolling.scroll_x, draw_y - Scrolling.scroll_y),
        )


##############
### Player ###
##############
class Player(Entity):
    def __init__(self, pos):
        super().__init__(
            size=(30, 50),
            image_path=str(ROOT_PATH / "assets" / "images" / "player.png"),
            default_pos=pos,
        )
        self.target_speed = 0
        self.air_time = time()
        self.air_time_grace_period = 1 / 15

        Logger.log("Created player")

    def move(self, world: World):
        speed_dif = self.target_speed - self.vx

        if self.target_speed == 0:
            self.vx += speed_dif / 6
        else:
            self.vx += speed_dif / 8

        super().move(world)
        try:
            return world.end_tile.rect.colliderect(self.rect) #kill me now
        except AttributeError:
            return False

    def event_handler(self):
        keys: dict = pygame.key.get_pressed()

        # Air time check (allowed to jump a bit after losing contact with ground)
        if self.collision_types["bottom"]:
            self.air_time = time()

        # Jump
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and (
            self.collision_types["bottom"]
            or time() - self.air_time < self.air_time_grace_period
        ):
            self.vy = -20

        # Right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.target_speed = 10

        # Left
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.target_speed = -10

        else:
            self.target_speed = 0

        # Other keys

        # Reset
        if keys[pygame.K_r]:
            self.vx = self.vy = 0
            self.rect.center = self.default_pos
