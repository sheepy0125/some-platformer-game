"""
Word class & data for Some Platformer Game
Created by sheepy0125
Source: https://youtu.be/abH2MSBdnWc
09/10/2021
"""

from pygame_setup import screen, pygame, SCREEN_SIZE
from utils import Logger, ROOT_PATH

# Scale tile size to have height fill all the way
# For now, we can agree that the height of the maps will be 10
MAP_HEIGHT = 10
TILE_SIZE = round(SCREEN_SIZE[1] / MAP_HEIGHT)

###################
### World class ###
###################
class World:
    """Handles all tiles in the world"""

    def __init__(self, data: list):
        self.data = data
        self.tile_map: list = []

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

                # Dirt
                if tile == 1:
                    self.tile_map.append(
                        Tile(
                            pos=tile_position,
                            image_path=str(
                                ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"
                            ),
                        )
                    )

                # TODO: more tiles

        Logger.log("Successfully created all tiles.")

    def draw_tiles(self):
        for tile in self.tile_map:
            tile.draw()


##################
### Tile class ###
##################
class Tile:
    """Base tile class"""

    def __init__(self, pos: tuple, image_path: str):
        self.x, self.y = pos
        self.scroll_x, self.scroll_y = (0, 0)
        self.image_path = image_path

        self.create()

    def __str__(self):
        return f"({self.x=},{self.y=}) {self.image_path=}"

    def create(self):
        self.surface = pygame.image.load(self.image_path).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (TILE_SIZE, TILE_SIZE))
        self.rect = self.surface.get_rect(left=self.x, top=self.y)

    def draw(self):
        screen.blit(self.surface, (self.x + self.scroll_x, self.y + self.scroll_y))


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
