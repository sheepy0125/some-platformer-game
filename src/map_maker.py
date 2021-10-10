"""
Map Maker for Some Platformer Game
Created by duuuck and sheepy0125
09/10/2012
"""

#############
### Setup ###
#############
# Import
import pygame
from pathlib import Path
from pygame_setup import *
from world import Tile, load_world, TILE_SIZE
from utils import Logger, ROOT_PATH

# Setup
tiles = []

#################
### Functions ###
#################
def snap_to_grid(location) -> list:
    return [(int(location[i] / TILE_SIZE) * TILE_SIZE) for i in range(2)]


def create_tile(mouse_pos):
    tiles.append(
        Tile(
            tile_pos := snap_to_grid(mouse_pos),
            image_path=str(ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"),
        )
    )
    Logger.log(f"Created tile at {tile_pos}")


def destroy_tile(mouse_pos):
    # Find the tile at the mouse position
    # Sure, I could use caching in a dict to make this process instant
    # But, too bad!
    tile_pos = snap_to_grid(mouse_pos)
    for tile_idx, tile in enumerate(tiles):
        if (tile.x, tile.y) == tuple(tile_pos):
            # That's the one!
            Logger.log(f"Removed the tile at {tile_pos}")
            tiles.pop(tile_idx)
            return

    Logger.fatal(f"No tile found at {tile_pos}")


def export():
    pass


############
### Main ###
############
while True:
    # Event handler
    for event in pygame.event.get():
        # Quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Creating
            if event.button == 1:
                create_tile((mouse_x, mouse_y))

            # Destroying
            else:
                destroy_tile((mouse_x, mouse_y))

    # Draw
    screen.fill("blue")
    for tile in tiles:
        tile.draw()
    pygame.display.update()
