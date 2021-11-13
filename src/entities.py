"""
Entities for Some Platformer Game
Created by duuuuck and sheepy0125
08/10/2021
"""

from pygame_setup import pygame, screen
from config_parser import GRAVITY
from utils import Logger, Scrolling, ROOT_PATH
from pygame_utils import CenterRect
from world import World
from sounds import play_sound
from time import time
from pathlib import Path


##############
### Entity ###
##############
class BaseEntity:
    """Base entity class"""

    def __init__(self, size: tuple, spritesheet_data: dict, default_pos: tuple):
        self.size = size
        self.default_pos = list(default_pos)

        self.spritesheet_data = spritesheet_data

        self.velocity_cap = (20, 10)
        self.vx = self.vy = 0
        self.direction = "forward"  # "forward" or "backward"

        self.land_time = time()
        self.prev_on_ground = False

        self.reset_collision_types()
        self.create()

    def __str__(self):
        return f"{self.size=} {self.image_path=} {self.movement_speed=}"

    def create(self):
        """Create surfaces from spritesheet"""

        for spritesheet_name, spritesheet_info in self.spritesheet_data.items():
            self.spritesheet_data[spritesheet_name]["spritesheet"] = SpriteSheet(
                image_path=spritesheet_info["image_path"],
                width_each=spritesheet_info["width_each"],
                conversion_size=self.size,
            )

            # Add last update time
            self.spritesheet_data[spritesheet_name]["last_update"] = time()

        self.current_spritesheet = "idle"
        self.rect = CenterRect(self.default_pos, self.size)

    def update(self):
        # If it's time for the spritesheet to be updated, do it
        if (
            time() - self.spritesheet_data[self.current_spritesheet]["last_update"]
            > self.spritesheet_data[self.current_spritesheet]["update_deltatime"]
        ):
            self.spritesheet_data[self.current_spritesheet]["last_update"] = time()
            self.update_spritesheet()

    def update_spritesheet(self):
        # Update spritesheet frame
        self.spritesheet_data[self.current_spritesheet]["spritesheet"].frame += 1
        # Assert the frame is in range
        if (self.spritesheet_data[self.current_spritesheet]["spritesheet"].frame) >= (
            self.spritesheet_data[self.current_spritesheet]["spritesheet"].total_frames
        ):
            self.spritesheet_data[self.current_spritesheet]["spritesheet"].frame = 0

    def move(self, world: World):
        self.reset_collision_types()

        # Horizontal

        # Add velocity
        if abs(self.vx > self.velocity_cap[0]):
            self.vx = self.velocity_cap[0]

        # Set position
        self.rect.x += round(self.vx)

        # Check horizontal collision
        collision_list = world.get_tile_collisions(self.rect)
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

            # Reset spritesheet
            self.current_spritesheet = "idle"

        # Vertical

        # Add velocity
        self.vy += GRAVITY * 1.5
        self.rect.y += self.vy

        # Check vertical collision
        collision_list = world.get_tile_collisions(self.rect)
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

    def reset_collision_types(self):
        self.collision_types = {
            "top": False,
            "bottom": False,
            "left": False,
            "right": False,
        }

    def draw(self):
        surface_to_blit = (
            self.spritesheet_data[self.current_spritesheet]["spritesheet"]
        ).surfaces[self.direction][
            self.spritesheet_data[self.current_spritesheet]["spritesheet"].frame
        ]

        # Draw current frame of the spritesheet
        screen.blit(
            surface_to_blit,
            (self.rect.x - Scrolling.scroll_x, self.rect.y - Scrolling.scroll_y),
        )


##############
### Player ###
##############
class Player(BaseEntity):
    def __init__(self, pos: tuple):
        # Create spritesheet data
        PLAYER_SPRITESHEET_IMAGES_DIR = ROOT_PATH / "assets" / "images" / "player"
        spritesheet_data = {
            "idle": {
                "image_path": str(PLAYER_SPRITESHEET_IMAGES_DIR / "idle.png"),
                "width_each": 10,
                "update_deltatime": 0.1,
            },
            "walk": {
                "image_path": str(PLAYER_SPRITESHEET_IMAGES_DIR / "walk.png"),
                "width_each": 10,
                "update_deltatime": 0.05,
            },
            "jump": {
                "image_path": str(PLAYER_SPRITESHEET_IMAGES_DIR / "jump.png"),
                "width_each": 10,
                "update_deltatime": 0.1,
            },
        }

        super().__init__(
            size=(30, 50),
            spritesheet_data=spritesheet_data,
            default_pos=pos,
        )
        self.target_speed = 0
        self.air_time = time()
        self.air_time_grace_period = 1 / 15

        Logger.log("Created player")

    def update(self, world: World):
        """Updates everything, extends from BaseEntity.update()"""
        super().update()

        self.move(world)
        self.event_handler()

    def move(self, world: World):
        speed_dif = self.target_speed - self.vx

        if self.target_speed == 0:
            self.vx += speed_dif / 6
        else:
            self.vx += speed_dif / 8

        super().move(world)

        # Check if collided with the ending tile
        if world.end_tile is not None and self.rect.colliderect(world.end_tile.rect):
            world.end_level()

    def event_handler(self):
        keys: dict = pygame.key.get_pressed()

        # Air time check (allowed to jump a bit after losing contact with ground)
        if self.collision_types["bottom"]:
            self.air_time = time()

        # Other keys

        # Reset
        if keys[pygame.K_r]:
            self.vx = self.vy = 0
            self.rect.center = self.default_pos

        # Movement

        # Jump
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and (
            self.collision_types["bottom"]
            or time() - self.air_time < self.air_time_grace_period
        ):
            play_sound("jump")
            self.vy = -20

        # Right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.target_speed = 10
            self.direction = "forward"

        # Left
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.target_speed = -10
            self.direction = "backward"

        else:
            self.target_speed = 0
            self.current_spritesheet = "idle"
            return

        self.current_spritesheet = "walk"


####################
### Sprite sheet ###
####################
class SpriteSheet:
    """
    Handles sprite sheet loading
    Currently we assume the spritesheet only had one row and that the width
    of each frame in the spritesheet is static, with no margins or padding
    """

    def __init__(self, image_path: Path, width_each: int, conversion_size: tuple):
        """
        :param image_path:       The path to the sprite sheet
        :param width_each:       The width of each frame of the spritesheet
        :param conversion_size:  The size each frame will be rendered as
        """

        self.image_path = image_path
        self.width_each = width_each
        self.conversion_size = conversion_size

        self.surfaces = self.create_surfaces()

        self.frame = 0
        self.total_frames = len(self.surfaces)

    def create_surfaces(self) -> dict:
        """Loads a spritesheet image and creates a list of surfaces from it"""

        main_image = pygame.image.load(self.image_path).convert_alpha()
        main_image_height = main_image.get_height()
        main_image_width = main_image.get_width()
        columns = main_image_width / self.width_each

        # Assert the number of columns is an integer
        if columns != int(columns):
            Logger.warn(
                f"The number of columns/frames in the spritesheet ({columns})"
                " is not an integer! This will result in clipped frames!"
            )

        # Floor it anyway
        columns = int(columns)

        # Create surfaces
        surfaces = {"forward": [], "backward": []}
        for column in range(columns):
            surface: pygame.Surface = pygame.transform.scale(
                main_image.subsurface(
                    pygame.Rect(
                        (column * self.width_each, 0),
                        (self.width_each, main_image_height),
                    )
                ),
                self.conversion_size,
            )

            # Right now, each frame is assumed to be facing backwards
            surfaces["forward"].append(
                pygame.transform.flip(surface, flip_x=True, flip_y=False)
            )
            surfaces["backward"].append(surface)

        return surfaces
