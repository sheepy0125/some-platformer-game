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

#######################
### Tiles dataclass ###
#######################
class Tiles:
    """Dataclass for tiles"""

    TILE_IMAGE_FOLDER = ROOT_PATH / "assets" / "images" / "tiles"

    tile_dict = {
        # For max_amount, -1 is infinite
        "1": {
            "filepath": str(TILE_IMAGE_FOLDER / "dirt.png"),
            "name": "dirt",
            "max_amount": -1,
        },
        "2": {
            "filepath": str(TILE_IMAGE_FOLDER / "stone.png"),
            "name": "Stone",
            "max_amount": -1,
        },
        "9": {
            "filepath": str(TILE_IMAGE_FOLDER / "player.png"),
            "name": "player",
            "max_amount": 1,
        },
    }


###################
### World class ###
###################
class World:
    """Handles all tiles in the world"""

    def __init__(self, map_list: list, player_pos: tuple):
        self.map_list: list = map_list
        self.player_pos = player_pos

    def draw_tiles(self):
        for tile in self.map_list:
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
def load_world(filepath) -> dict:
    """Returns a 2D array of Tiles"""

    def not_valid_tile_warn(x: int, y: int, tile: str):
        """Warns that the tile isn't valid"""

        Logger.warn(
            f"The tile at position ({x}, {y}) is {tile}, which is not a valid tile!"
        )

    with open(filepath) as world_file:
        world_file_str = world_file.read()

    map_list = world_file_str.split("\n")
    tiles: list[Tile] = []
    player_pos = None
    for row_idx, row in enumerate(map_list):
        for tile_idx, tile in enumerate(row):
            # The tile is air
            if int(tile) == 0:
                Logger.log("The tile is air")
                continue

            # tile_idx is x multiplier
            # row_idx is y multiplier
            # Positions are bound to top left
            tile_position = (tile_idx * TILE_SIZE, row_idx * TILE_SIZE)

            # Normal tiles
            if int(tile) < 8:
                # Assert the tile is a valid tile
                if not tile in Tiles.tile_dict:
                    not_valid_tile_warn(row_idx, tile_idx, tile)
                    continue

                # Create tile
                tile_instance = Tile(
                    pos=tile_position,
                    image_path=Tiles.tile_dict[tile]["filepath"],
                    id=tile,
                )
                tiles.append(tile_instance)
                continue

            # Player position tile
            if tile == 9:
                player_pos = (
                    tile_position[0] + TILE_SIZE // 2,
                    tile_position[1] + TILE_SIZE // 2,
                )
                continue

            not_valid_tile_warn(row_idx, tile_idx, tile)

    # No player position tile
    if player_pos is None:
        Logger.warn("No player tile set, using default position")
        player_pos = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

    print(len(tiles))
    for tile in tiles:
        print(tile.id)

    return {"map_list": tiles, "player_pos": player_pos}
