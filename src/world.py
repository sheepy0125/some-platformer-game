"""
Word class & data for Some Platformer Game
Created by sheepy0125
Source: https://youtu.be/abH2MSBdnWc
09/10/2021
"""

from pygame_setup import pygame, screen, SCREEN_SIZE
from utils import Logger, Scrolling, ROOT_PATH
from typing import Union

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
            "filepath": str(TILE_IMAGE_FOLDER / "grass.png"),
            "name": "grass",
            "max_amount": -1,
        },
        "2": {
            "filepath": str(TILE_IMAGE_FOLDER / "dirt.png"),
            "name": "dirt",
            "max_amount": -1,
        },
        "3": {
            "filepath": str(TILE_IMAGE_FOLDER / "stone.png"),
            "name": "stone",
            "max_amount": -1,
        },
        "8": {
            "filepath": str(TILE_IMAGE_FOLDER / "end.png"),
            "name": "end",
            "max_amount": 1,
        },
        "9": {
            "filepath": str(TILE_IMAGE_FOLDER / "player.png"),
            "name": "player",
            "max_amount": 1,
        },
        "_tile_not_found": {
            "filepath": str(TILE_IMAGE_FOLDER / "error.png"),
            "name": "TILE_NOT_FOUND",
            "max_amount": -1,
        },
    }


###################
### World class ###
###################
class World:
    """Handles all tiles in the world"""

    def __init__(
        self, map_array: list[list], player_pos: tuple, end_tile_pos: Union[tuple, None]
    ):
        self.map_array = map_array
        self.map_list = convert_map_to_list(map_array)
        self.player_pos = player_pos
        # Create end tile
        self.end_tile = (
            (Tile(pos=end_tile_pos, image_path=Tiles.tile_dict["8"]["filepath"], id=8))
            if end_tile_pos is not None
            else None
        )

    def get_tile_collisions_new(self, player_rect: pygame.Rect) -> list:
        # Get the tiles around the player (there should be 8 maximum!)
        # Use the 2d tile array and the player position snapped to tile index grid to
        # find the tiles around the player
        # Then check collisions for all of those tiles

        collided_tiles = []
        nearest_neighbour_tiles = []
        player_pos_snapped_to_grid = snap_to_grid(player_rect.center)
        player_pos_array_idx = get_tile_idx(
            player_pos_snapped_to_grid,
            map_size=(len(self.map_array[1]), len(self.map_array)),
        )

        # Get the tiles around the player
        for y_offset in range(-1, 3):  # Above, at top, at bottom, below
            for x_offset in range(-1, 2):  # Left, at, right
                try:
                    nearest_neighbour_tiles.append(
                        self.map_array[player_pos_array_idx[1] + y_offset][
                            player_pos_array_idx[0] + x_offset
                        ]
                    )
                    Logger.log(
                        "Added nearest neighbor tile at "
                        f"({player_pos_array_idx[0] + y_offset},"
                        f"{player_pos_array_idx[1] + x_offset})"
                    )
                except IndexError:
                    """
                    An IndexError occurs when the player is near or
                    outside of the border, it's nothing to worry about
                    """
                    pass

        Logger.log(f"The player index is {player_pos_array_idx}")

        # Check collisions for all of those tiles
        for tile in nearest_neighbour_tiles:
            # Assert the tile is not NoneType (air)
            if tile is None:
                continue

            if tile.rect.colliderect(player_rect):
                Logger.log(f"Collision with tile {tile.id}")
                collided_tiles.append(tile)

        return collided_tiles

    def get_tile_collisions_old(self, player_rect) -> list:
        return [
            tile_rect
            for tile_rect in self.map_list
            if player_rect.colliderect(tile_rect)
        ]

    def end_level(self):
        Logger.log("The player has touched the end of the level, oh well")

    def draw_tiles(self):
        for tile in self.map_list:
            tile.draw()

        if self.end_tile is not None:
            self.end_tile.draw()


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
        if (
            self.x - Scrolling.scroll_x < SCREEN_SIZE[0]
            and self.x + TILE_SIZE - Scrolling.scroll_x > 0
        ):
            if (
                self.y - Scrolling.scroll_y < SCREEN_SIZE[1]
                and self.y + TILE_SIZE - Scrolling.scroll_y > 0
            ):
                screen.blit(
                    self.surface,
                    (self.x - Scrolling.scroll_x, self.y - Scrolling.scroll_y),
                )


#################
### Functions ###
#################
def load_map(filepath) -> dict:
    """Returns a 2D array of Tiles"""

    def not_valid_tile_warn(x: int, y: int, tile: str):
        """Warns that the tile isn't valid"""

        Logger.warn(
            f"The tile at position ({x}, {y}) is {tile}, which is not a valid tile!"
        )

    with open(filepath) as world_file:
        map_file_str = world_file.read()

    map_array: list[Tile] = []
    player_pos = None
    end_tile_pos = None
    for row_idx, row in enumerate(map_file_str.split("\n")):
        map_array.append([])
        for tile_idx, tile in enumerate(row):
            # The tile is air
            if int(tile) == 0:
                map_array[row_idx].append(None)
                continue

            # tile_idx is x multiplier
            # row_idx is y multiplier
            # Positions are bound to top left
            tile_position = (tile_idx * TILE_SIZE, row_idx * TILE_SIZE)

            # Normal tiles

            if int(tile) < 7:
                # Assert the tile is a valid tile
                if not tile in Tiles.tile_dict:
                    not_valid_tile_warn(row_idx, tile_idx, tile)
                    tile = "_tile_not_found"

                # Create tile
                tile_instance = Tile(
                    pos=tile_position,
                    image_path=Tiles.tile_dict[tile]["filepath"],
                    id=tile,
                )
                map_array[row_idx].append(tile_instance)
                continue

            # Ending tile
            if int(tile) == 8:
                end_tile_pos = tile_position
                continue

            # Player position tile
            if int(tile) == 9:
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

    if end_tile_pos is None:
        Logger.warn("No exit location, player trapped inside level forever")

    return {"map_array": map_array, "player_pos": player_pos, "end_tile": end_tile_pos}


def convert_map_to_list(map_array: list[list]) -> list:
    """Converts the 2D array to a list"""

    return_list = []
    for row in map_array:
        for tile in row:
            # Assert the tile is not NoneType
            if tile is None:
                continue
            return_list.append(tile)

    return return_list


def snap_to_grid(mouse_pos: tuple) -> tuple:
    """Returns the top left coordinate of a tile from a mouse position"""

    return tuple([(int(mouse_pos[i] / TILE_SIZE) * TILE_SIZE) for i in range(2)])


def get_tile_idx(tile_location: tuple, map_size: tuple) -> tuple:
    """
    Get the tile indecies of a tile location (top left)
    Returns a tuple with the first index being the row index and the
    second index being the column index (it's a 2D map)
    """

    tile_idx = (
        int((tile_location[0]) // TILE_SIZE),
        int((tile_location[1]) // TILE_SIZE),
    )

    # Assert tile is in bounds
    if ((tile_idx[0] < 0) or (tile_idx[0] >= map_size[0])) or (
        (tile_idx[1] < 0) or (tile_idx[1] >= map_size[1])
    ):
        Logger.fatal(f"Tile is out of bounds ({tile_idx})!")

    return tile_idx
