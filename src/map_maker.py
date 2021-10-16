"""
Map Maker for Some Platformer Game
Created by duuuck and sheepy0125
09/10/2012
"""

#############
### Setup ###
#############
# Import
# FIXME: fix imports
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog
from tkinter.ttk import Spinbox
from pygame_setup import pygame, screen, clock, SCREEN_SIZE
from world import Tile, load_world, TILE_SIZE
from pygame_utils import Text
from utils import Logger, Scrolling, ROOT_PATH

# Setup
pygame.display.set_caption("Map maker for Some Platformer Game")

###############
### Classes ###
###############
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
        ((tile_location[0] + Scrolling.scroll_x) // TILE_SIZE),
        (tile_location[1] // TILE_SIZE),
    )
    return tile_idx


def tile_exists(tile_pos: tuple, tile_idx: tuple):
    return TileMap.tile_map[tile_idx[1]][tile_idx[0]] is not None


def create_tile(mouse_pos):
    tile_pos = snap_to_grid(mouse_pos)
    tile_idx = get_tile_idx(tile_pos)
    if tile_exists(tile_pos, tile_idx):
        return

    TileMap.tile_map[tile_idx[1]][tile_idx[0]] = Tile(
        (tile_pos[0] + Scrolling.scroll_x, tile_pos[1] + Scrolling.scroll_y),
        image_path=str(ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"),
        id=1,
    )


def destroy_tile(mouse_pos):
    tile_idx = get_tile_idx(snap_to_grid(mouse_pos))
    TileMap.tile_map[tile_idx[1]][tile_idx[0]] = None


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
    def save_variables() -> bool | int:
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

    width_spinbox = Spinbox(root, from_=20, to=500)
    height_spinbox = Spinbox(
        root, from_=10, to=10
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
        (SCREEN_SIZE[0] // TILE_SIZE)
    ) * TILE_SIZE
    print(max_scroll_x)

    TileMap.create_tile_2d_array(map_size)

    texts = [
        Text(
            "Map Maker for Some Platformer Game",
            size=12,
            pos=(SCREEN_SIZE[0] // 2, 15),
        ),
        Text("Press H to toggle this text", size=12, pos=(SCREEN_SIZE[0] // 2, 30)),
        Text("Press R to reset", size=12, pos=(SCREEN_SIZE[0] // 2, 45)),
        Text("Press the arrow keys to scroll", size=12, pos=(SCREEN_SIZE[0] // 2, 60)),
    ]
    currently_scrolling_text = Text(
        f"Currently scrolling {Scrolling.scroll_x // TILE_SIZE} times",
        size=12,
        pos=(SCREEN_SIZE[0] // 2, 75),
    )
    show_text = True
    while True:
        # Event handler
        for event in pygame.event.get():
            # Quitting
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # Keypress
            if event.type == pygame.KEYUP:
                # Toggle text
                if event.key == pygame.K_h:
                    show_text = not show_text

                # Reset map
                elif event.key == pygame.K_r:
                    TileMap.create_tile_2d_array(map_size)

                # Scroll screen to the right
                if event.key == pygame.K_RIGHT:
                    if Scrolling.scroll_x < max_scroll_x:
                        Scrolling.scroll_x += TILE_SIZE

                # Scroll screen to the left
                elif event.key == pygame.K_LEFT:
                    if Scrolling.scroll_x != 0:
                        Scrolling.scroll_x -= TILE_SIZE

                elif event.key == pygame.K_e:
                    try:
                        pass
                    except Exception as error:
                        Logger.fatal("Failed to export map")
                        Logger.log_error(error)
                    export(TileMap.tile_map)

                # Not scrolling
                else:
                    break

                # Update scrolled text
                currently_scrolling_text = Text(
                    f"Currently scrolling {Scrolling.scroll_x} pixels "
                    + f"({Scrolling.scroll_x // TILE_SIZE} times out of "
                    + f"{max_scroll_x // TILE_SIZE})",
                    size=12,
                    pos=(SCREEN_SIZE[0] // 2, 75),
                )

        # Mouse click
        if (buttons_pressed := pygame.mouse.get_pressed()) != (0, 0, 0):
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Creating
            if buttons_pressed[0]:
                create_tile((mouse_x, mouse_y))

            # Destroying
            else:
                destroy_tile((mouse_x, mouse_y))

        # Draw
        screen.fill("blue")
        for tile_row in TileMap.tile_map:  # 2D Array, so both row and tile
            for tile in tile_row:
                if tile is not None:
                    tile.draw()

        if show_text:
            for text in texts:
                text.draw()
            currently_scrolling_text.draw()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
