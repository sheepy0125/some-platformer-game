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
from tkinter import Tk, Label, Button, filedialog
from tkinter.ttk import Spinbox
from world import Tile, TILE_SIZE, Tiles as WorldTiles
from pygame_utils import Text
from utils import Logger, Scrolling, ROOT_PATH

SCREEN_SIZE = (800, 800)
SIDEBAR_SIZE = (200, 800)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Setup
pygame.display.set_caption("Map maker for Some Platformer Game")

###############
### Classes ###
###############
class Tiles:
    """
    Tiles class which inherits from the Tiles class in world.py, but now
    works for the map maker
    Note: Doesn't actually use inheritance, just stores a copy of the tile dict
    We're doing this because we don't wanna use super() to call it, nor use
    a getter / setter for it
    """

    tile_dict = WorldTiles.tile_dict

    current_tile = 1
    # Set amount of tiles
    total_tiles = 0
    for tile_id in tile_dict.keys():
        tile_dict[tile_id]["amount"] = 0

    # Change tile
    @staticmethod
    def change_tile(next_tile: bool):
        """
        Changes to a new tile
        next_tile: Tells whether we are switching forwards or backwards
        """

        # Get the new tile ID from the dictionary keys
        # We need to do this because tile indeces are not (always) sequential
        tile_keys = list(Tiles.tile_dict.keys())
        current_tile_index = tile_keys.index(str(Tiles.current_tile))
        # Find the index of the new tile
        if next_tile:
            new_tile_index = current_tile_index + 1
            # Out of bounds check
            if new_tile_index >= len(tile_keys):
                new_tile_index = 0
        else:
            new_tile_index = current_tile_index - 1
            # Out of bounds check
            if new_tile_index < 0:
                new_tile_index = len(tile_keys) - 1

        # Get the new tile tile ID
        new_tile_id = tile_keys[new_tile_index]

        Tiles.current_tile = new_tile_id


class TileMap:
    tile_map = []

    @staticmethod
    def create_tile_2d_array(map_size: tuple) -> list[list]:
        tile_map = []
        # Rows
        for _ in range(map_size[1]):
            # Create list of zeros
            tile_map.append([None for _ in range(map_size[0])])

        TileMap.tile_map = tile_map
        Logger.log("Created tile map")

    @staticmethod
    def convert_array_to_string() -> str:
        """Converts the tile map array into a string for saving and debug prints"""

        map_str = ""

        for row in TileMap.tile_map:
            for tile in row:
                if tile is None:
                    map_str += "0"
                else:
                    map_str += str(tile.id)
            map_str += "\n"

        return map_str

    @staticmethod
    def debug_print() -> None:
        """Prints the tile map array for debug purposes"""

        Logger.log("Debugging print the tile map")

        for row_idx, row in enumerate(
            TileMap.convert_array_to_string().split("\n")[:-1]
        ):
            Logger.log(f"Row {row_idx:3d}: {row}")


class Sidebar:
    def __init__(self):
        # Background
        self.background_rect = pygame.Rect((0, 0), (SIDEBAR_SIZE[0], SIDEBAR_SIZE[1]))

        # Texts
        self.texts = [
            Text(
                "Map Maker!",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 15),
            ),
            Text(
                "LMB: Place, RMB: Destroy",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 30),
            ),
            Text(
                "Press the arrow keys to scroll",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 45),
            ),
            Text(
                "Press R to reset",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 60),
            ),
            Text(
                "Press E to export",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 75),
            ),
            Text(
                "Press P to debug print the map",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 90),
            ),
            Text(
                "Press N to switch to the next block",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 105),
            ),
            Text(
                "Press B to switch to the prev block",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 120),
            ),
            Text(
                "Available tiles",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 210 + 128),
            ),
            Text(
                f"{MapSize.size[0]}x{MapSize.size[1]}",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, SIDEBAR_SIZE[1] - 15),
            ),
        ]
        self.create_scroll_text()
        self.create_current_tile_widgets()
        self.create_total_tiles_text()

        # Available tile texts
        self.available_tile_texts = []
        for tile_idx, (tile_id, available_tile) in enumerate(Tiles.tile_dict.items()):
            # Please note: tile_id is a string, not an int
            self.available_tile_texts.append(
                Text(
                    f"Tile {tile_id}: {available_tile['name']}",
                    size=12,
                    pos=(SIDEBAR_SIZE[0] // 2, (225 + 128 + (15 * tile_idx))),
                )
            )

    def create_scroll_text(self):
        self.currently_scrolling_text = Text(
            f"Scroll X: {Scrolling.scroll_x} | Scroll Y: {Scrolling.scroll_y}",
            size=12,
            pos=(SIDEBAR_SIZE[0] // 2, 150),
        )

    def create_current_tile_widgets(self):
        self.current_tile_text = Text(
            f"Current tile: {Tiles.tile_dict[str(Tiles.current_tile)]['name']}",
            size=12,
            pos=(SIDEBAR_SIZE[0] // 2, 180),
        )
        self.current_tile_image = pygame.transform.scale(
            pygame.image.load(Tiles.tile_dict[str(Tiles.current_tile)]["filepath"]),
            (128, 128),
        )
        self.current_tile_image_rect = self.current_tile_image.get_rect(
            centerx=(SIDEBAR_SIZE[0] // 2), top=195
        )

    def create_total_tiles_text(self):
        self.total_tiles_text = Text(
            f"Total tiles: {Tiles.total_tiles}",
            size=12,
            pos=(SIDEBAR_SIZE[0] // 2, SIDEBAR_SIZE[1] - 30),
        )

    def draw(self):
        pygame.draw.rect(screen, rect=self.background_rect, color="black")
        for text in self.texts:
            text.draw()
        for text in self.available_tile_texts:
            text.draw()
        self.currently_scrolling_text.draw()
        self.current_tile_text.draw()
        self.total_tiles_text.draw()
        screen.blit(self.current_tile_image, self.current_tile_image_rect)


#################
### Functions ###
#################
def snap_to_grid(mouse_pos: tuple) -> tuple:
    """Returns the top left coordinate of a tile from a mouse position"""

    return tuple([(int(mouse_pos[i] / TILE_SIZE) * TILE_SIZE) for i in range(2)])


def get_tile_idx(tile_location: tuple) -> tuple:
    """
    Get the tile indecies of a tile location (top left)
    Returns a tuple with the first index being the row index and the
    second index being the column index (it's a 2D map)
    """

    tile_idx = (
        ((tile_location[0] + Scrolling.scroll_x) // TILE_SIZE)
        - SIDEBAR_SIZE[0] // TILE_SIZE,
        (tile_location[1] + Scrolling.scroll_y) // TILE_SIZE,
    )

    # Assert tile is in bounds
    if ((tile_idx[0] < 0) or (tile_idx[0] >= MapSize.size[0])) or (
        (tile_idx[1] < 0) or (tile_idx[1] >= MapSize.size[1])
    ):
        Logger.fatal(f"Tile is out of bounds ({tile_idx})!")

    return tile_idx


def tile_exists(tile_idx: tuple):
    return TileMap.tile_map[tile_idx[1]][tile_idx[0]] is not None


def create_tile(mouse_pos):
    tile_pos = snap_to_grid(mouse_pos)
    tile_idx = get_tile_idx(tile_pos)
    if tile_exists(tile_idx):
        return

    # Don't allow creation of tile if the max number of tiles has been reached for that tile
    if (
        max_num_of_tiles := Tiles.tile_dict[str(Tiles.current_tile)]["max_amount"]
    ) != -1:
        if max_num_of_tiles <= Tiles.tile_dict[str(Tiles.current_tile)]["amount"]:
            Logger.warn(f"Can't create more than {max_num_of_tiles} of this tile!")
            return

    # Get tile filepath and ID
    tile_id = Tiles.current_tile
    tile_image_filepath = Tiles.tile_dict[str(tile_id)]["filepath"]

    TileMap.tile_map[tile_idx[1]][tile_idx[0]] = Tile(
        (
            tile_pos[0] + Scrolling.scroll_x,
            tile_pos[1] + Scrolling.scroll_y,
        ),
        image_path=tile_image_filepath,
        id=tile_id,
    )
    Tiles.total_tiles += 1
    Tiles.tile_dict[str(tile_id)]["amount"] += 1


def destroy_tile(mouse_pos):
    tile_pos = snap_to_grid(mouse_pos)
    tile_idx = get_tile_idx(tile_pos)
    if not tile_exists(tile_idx):
        return

    tile_id = TileMap.tile_map[tile_idx[1]][tile_idx[0]].id
    TileMap.tile_map[tile_idx[1]][tile_idx[0]] = None

    Tiles.total_tiles -= 1
    Tiles.tile_dict[str(tile_id)]["amount"] -= 1


def export():
    """Save tile to a file"""

    map_string = TileMap.convert_array_to_string()

    # Get filepath to export to
    map_file = filedialog.asksaveasfile()
    Logger.log(f"Exporting map to {map_file.name}")

    with map_file:
        map_file.truncate(0)
        map_file.write(map_string)

    Logger.log("Successfully exported map")


#################
### Map setup ###
#################
class MapSize:
    size = (0, 0)


def map_setup() -> tuple:
    def save_variables() -> int:
        try:
            assert (
                width := width_spinbox.get()
            ) != "", "Width parameter must not be empty"
            assert (
                height := height_spinbox.get()
            ) != "", "Height parameter must not be empty"

            root.destroy()

        except Exception as error:
            Logger.log_error(error)
            return

        MapSize.size = (int(width), int(height))

    root = Tk()
    root.geometry("300x200")
    root.title("Map maker setup")

    Label(root, text="Map maker setup").pack(pady=2)

    width_spinbox = Spinbox(
        root, from_=round((SCREEN_SIZE[0] - SIDEBAR_SIZE[0]) / TILE_SIZE), to=500
    )
    height_spinbox = Spinbox(
        root, from_=round(SCREEN_SIZE[1] // TILE_SIZE), to=500
    )  # TODO: scrolling vertically instead of fixed

    Label(root, text="Width").pack(pady=2)
    width_spinbox.pack(pady=2)
    Label(root, text="Height").pack(pady=2)
    height_spinbox.pack(
        pady=2,
    )

    Button(root, text="Go!", command=save_variables).pack(pady=2)

    root.mainloop()

    Logger.log(f"Map size is {MapSize.size}")
    return MapSize.size


############
### Main ###
############
def main():
    map_size = map_setup()
    max_scroll_x = (map_size[0] * TILE_SIZE) - (
        (SCREEN_SIZE[0] - SIDEBAR_SIZE[0]) // TILE_SIZE
    ) * TILE_SIZE
    max_scroll_y = (map_size[1] * TILE_SIZE) - (SCREEN_SIZE[1])
    Scrolling.scroll_y = max_scroll_y

    sidebar = Sidebar()
    TileMap.create_tile_2d_array(map_size)

    while True:
        # Event handler
        for event in pygame.event.get():
            # Quitting
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # Keypress
            if event.type == pygame.KEYUP:
                # Reset map
                if event.key == pygame.K_r:
                    # Reset tile map
                    TileMap.create_tile_2d_array(map_size)
                    Tiles.total_tiles = 0
                    for tile_id in Tiles.tile_dict:
                        Tiles.tile_dict[tile_id]["amount"] = 0
                    # Reset sidebar
                    sidebar.create_total_tiles_text()

                # Debug print
                elif event.key == pygame.K_p:
                    TileMap.debug_print()

                # Export
                elif event.key == pygame.K_e:
                    try:
                        export()
                    except Exception as error:
                        Logger.fatal("Failed to export map")
                        Logger.log_error(error)

                # Tile switching
                while True:
                    # Switch to next block
                    if event.key == pygame.K_n:
                        Tiles.change_tile(True)
                    # Switch to previous block
                    elif event.key == pygame.K_b:
                        Tiles.change_tile(False)

                    # Didn't switch tile
                    else:
                        break

                    # Switched block, recreate for sidebar
                    sidebar.create_current_tile_widgets()
                    sidebar.create_total_tiles_text()
                    break

                # Scrolling

                # Scroll screen to the right
                if event.key == pygame.K_RIGHT:
                    if Scrolling.scroll_x < max_scroll_x:
                        Scrolling.scroll_x += TILE_SIZE

                # Scroll screen to the left
                elif event.key == pygame.K_LEFT:
                    if Scrolling.scroll_x != 0:
                        Scrolling.scroll_x -= TILE_SIZE

                # Scroll screen up
                elif event.key == pygame.K_UP:
                    if Scrolling.scroll_y > 0:
                        Scrolling.scroll_y -= TILE_SIZE

                # Scroll screen down
                elif event.key == pygame.K_DOWN:
                    if Scrolling.scroll_y < max_scroll_y:
                        Scrolling.scroll_y += TILE_SIZE

                # Not scrolling
                else:
                    break

                # Update text
                sidebar.create_scroll_text()

        # Mouse click
        if (buttons_pressed := pygame.mouse.get_pressed()) != (0, 0, 0):
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Not on sidebar
            if mouse_x > SIDEBAR_SIZE[0]:
                # Creating
                if buttons_pressed[0]:
                    create_tile((mouse_x, mouse_y))

                # Destroying
                else:
                    destroy_tile((mouse_x, mouse_y))

                sidebar.create_total_tiles_text()

        # Draw
        screen.fill("blue")
        for tile_row in TileMap.tile_map:  # 2D Array, so both row and tile
            for tile in tile_row:
                if tile is not None:
                    tile.draw()

        sidebar.draw()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
