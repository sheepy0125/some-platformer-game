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
from world import Tile, load_world, TILE_SIZE
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
    tile_dict = {
        "1": {
            "filepath": str(ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"),
            "name": "dirt",
        }
    }
    current_tile = 1
    total_tiles = 0


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
                "Press E to Export",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 75),
            ),
            Text(
                "Press N to switch to the next block",
                size=12,
                pos=(SIDEBAR_SIZE[0] // 2, 105),
            ),
            Text(
                "Press P to switch to the prev block",
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
        for tile_idx, available_tile in enumerate(Tiles.tile_dict.values()):
            print(tile_idx, available_tile)
            self.available_tile_texts.append(
                Text(
                    f"Tile {tile_idx + 1}: {available_tile['name']}",
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

    return (
        ((tile_location[0] + Scrolling.scroll_x) // TILE_SIZE)
        - SIDEBAR_SIZE[0] // TILE_SIZE,
        (tile_location[1] + Scrolling.scroll_y) // TILE_SIZE,
    )


def tile_exists(tile_pos: tuple, tile_idx: tuple):
    return TileMap.tile_map[tile_idx[1]][tile_idx[0]] is not None


def create_tile(mouse_pos):
    tile_pos = snap_to_grid(mouse_pos)
    tile_idx = get_tile_idx(tile_pos)
    if tile_exists(tile_pos, tile_idx):
        return

    TileMap.tile_map[tile_idx[1]][tile_idx[0]] = Tile(
        (
            tile_pos[0] + Scrolling.scroll_x,
            tile_pos[1] + Scrolling.scroll_y,
        ),
        image_path=str(ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"),
        id=1,
    )
    Tiles.total_tiles += 1


def destroy_tile(mouse_pos):
    tile_pos = snap_to_grid(mouse_pos)
    tile_idx = get_tile_idx(tile_pos)
    if not tile_exists(tile_pos, tile_idx):
        return

    TileMap.tile_map[tile_idx[1]][tile_idx[0]] = None
    Tiles.total_tiles -= 1


def export(tiles):
    # Map string
    export_text = ""
    for tile_row in TileMap.tile_map:
        for tile in tile_row:
            # Tile doesn't exist (air)
            if tile is None:
                export_text += "0"
                continue

            # Use tile ID
            export_text += str(tile.id)

        export_text += "\n"

    # Get filepath to export to
    map_file = filedialog.asksaveasfile()
    Logger.log(f"Exporting map to {map_file.name}")

    with map_file:
        map_file.truncate(0)
        map_file.write(export_text)

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
    max_scroll_y = -(map_size[1] * TILE_SIZE)

    print(max_scroll_y)

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
                    TileMap.create_tile_2d_array(map_size)
                    Tiles.total_tiles = 0
                    sidebar.create_total_tiles_text()

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
                    if Scrolling.scroll_y > max_scroll_y:
                        Scrolling.scroll_y -= TILE_SIZE

                # Scroll screen down
                elif event.key == pygame.K_DOWN:
                    if Scrolling.scroll_y != 0:
                        Scrolling.scroll_y += TILE_SIZE

                elif event.key == pygame.K_e:
                    try:
                        export(TileMap.tile_map)
                    except Exception as error:
                        Logger.fatal("Failed to export map")
                        Logger.log_error(error)

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
