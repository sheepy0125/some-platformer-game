"""
Word class & data for Some Platformer Game
Created by sheepy0125
Source: https://youtu.be/abH2MSBdnWc
09/10/2021
"""

from pygame_setup import pygame, screen, SCREEN_SIZE
from utils import Logger, Scrolling, ROOT_PATH

MAP_HEIGHT = 10
TILE_SIZE = 50


class Tiles:
    """Dataclass for tiles"""

    tile_dict = {
        # For max_amount, -1 is infinite
        "1": {
            "filepath": str(ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"),
            "name": "dirt",
            "max_amount": -1,
        },
        "9": {
            "filepath": str(ROOT_PATH / "assets" / "images" / "tiles" / "player.png"),
            "name": "player",
            "max_amount": 1,
        },
    }


###################
### World class ###
###################
class World:
    """Handles all tiles in the world"""

    def __init__(self, data: list):
        self.data = data
        self.tile_map: list = []
        self.player_pos = None

        self.create_tiles()

    def create_tiles(self):
        for row_idx, row in enumerate(self.data):
            for tile_idx, tile in enumerate(row):
                # NOTE: tile is an int

                # Don't need to draw any tiles if it's air
                if tile == 0:
                    continue

                # tile_idx is x multiplier
                # row_idx is y multiplier
                # Positions are bound to top left
                tile_position = (tile_idx * TILE_SIZE, row_idx * TILE_SIZE)

                # Normal tiles (1-8)
                if tile < 8:
                    self.tile_map.append(
                        Tile(
                            pos=tile_position,
                            image_path=Tiles.tile_dict[str(tile)]["filepath"],
                            id=tile,
                        )
                    )

                # Player tile
                if tile == 9:
                    # Convert top left of tile posititon to center
                    self.player_pos = (
                        tile_position[0] + TILE_SIZE // 2,
                        tile_position[1] + TILE_SIZE // 2,
                    )

                # TODO: more normal tiles

        if self.player_pos is None:
            Logger.warn("No player tile set, using default position")
            self.player_pos = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

        Logger.log("Successfully created all tiles")

    def draw_tiles(self):
        for tile in self.tile_map:
            tile.draw()


##################
### Tile class ###
##################
class Tile:
    """Base tile class"""

    def __init__(self, pos: tuple, image_path: str, id: int):
        self.x, self.y = pos
        self.image_path = image_path
        self.id = id

        self.create()

    def __str__(self):
        return f"({self.x=},{self.y=}) {self.scroll_x=},{self.scroll_y=} {self.image_path=}"

    def create(self):
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (TILE_SIZE, TILE_SIZE))
        self.rect = self.surface.get_rect(left=self.x, top=self.y)

    def draw(self):
        screen.blit(
            self.surface, (self.x - Scrolling.scroll_x, self.y - Scrolling.scroll_y)
        )


####################
### World loader ###
####################
def load_world(filepath) -> list:
    # Assume the world file consists of 60x10 of 0s and 1s
    data_array: list = []
    with open(filepath) as world_file:
        rows: list = world_file.readlines()
        # Iterate through rows
        for row_idx in range(len(rows)):
            data_array.append([])
            row_text: str = rows[row_idx]
            # Iterate through tiles
            for tile_text in row_text:
                # If new line, don't bother
                if tile_text == "\n":
                    continue

                tile: int = int(tile_text)

                # Append
                data_array[row_idx].append(tile)

    if (row_num := len(data_array)) < 10:
        Logger.warn(f"Data array has under 10 rows (has {row_num} rows)")
    else:
        Logger.log(f"Data array has {row_num} rows")

    Logger.log("Succesfully loaded world")
    return data_array
