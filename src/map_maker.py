"""
Map Maker for Some Platformer Game
Created by duuuck and sheepy0125
09/10/2012
"""

#############
### Setup ###
#############
# Import
from pathlib import Path
from tkinter import Tk, Label, Button
from tkinter.ttk import Spinbox
from pygame_setup import *
from world import Tile, load_world, TILE_SIZE
from pygame_utils import Text
from utils import Logger, Scrolling, ROOT_PATH

# Setup
pygame.display.set_caption("Map maker for Some Platformer Game")
tiles = []
Scrolling.scroll_x = 0

#################
### Functions ###
#################
def snap_to_grid(location) -> list:
    return tuple([(int(location[i] / TILE_SIZE) * TILE_SIZE) for i in range(2)])


def find_tile(tile_pos):
    """Only finds the first tile"""

    for tile_idx, tile in enumerate(tiles):
        if (tile.x - tile.scroll_x, tile.y) == tuple(tile_pos):
            return tile_idx

    return False


def tile_exists(tile_pos):
    for tile in tiles:
        if tile.rect.topleft == tile_pos:
            return True

    return False


def create_tile(mouse_pos):
    mouse_pos = list(mouse_pos)
    mouse_pos[0] += Scrolling.scroll_x
    tile_pos = snap_to_grid(mouse_pos)
    if tile_exists(tile_pos):
        return

    tiles.append(
        Tile(
            tile_pos,
            image_path=str(ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"),
            id=1,
        )
    )


def destroy_tile(mouse_pos):
    tile_pos = snap_to_grid(mouse_pos)
    if tile_idx := find_tile(tile_pos):
        tiles.pop(tile_idx)


def export(tiles):
    # export tiles into
    id_map = {}
    far_tile_coords = [0, 0]

    for tile in tiles:
        if far_tile_coords[0] < tile.x:
            far_tile_coords[0] = tile.x
        if far_tile_coords[1] < tile.y:
            far_tile_coords[1] = tile.y

        id_map[(tile.x // TILE_SIZE, tile.y // TILE_SIZE)] = tile.id

    map_size = (
        far_tile_coords[0] // TILE_SIZE,
        far_tile_coords[1] // TILE_SIZE,
    )  # get map tile width and height

    file_text = ""

    for i in range(map_size[0]):
        for j in range(map_size[1]):
            try:
                file_text += str(id_map[(i, j)])
            except KeyError:
                file_text += "0"

        file_text += "\n"

    f = open("export.map", "x")
    f.write(file_text)

    return map_size


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

    width_spinbox = Spinbox(root, from_=20, to=60)
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

    return MapSize.size


############
### Main ###
############
def main():
    map_size = map_setup()
    print(map_size)
    max_scroll_x = map_size[0] * TILE_SIZE

    texts = [
        Text(
            "Map Maker for Some Platformer Game",
            size=12,
            pos=(SCREEN_SIZE[0] // 2, 15),
        ),
        Text("Press H to toggle this text", size=12, pos=(SCREEN_SIZE[0] // 2, 30)),
        Text("Press the arrow keys to scroll", size=12, pos=(SCREEN_SIZE[0] // 2, 45)),
    ]
    currently_scrolling_text = Text(
        f"Currently scrolling {Scrolling.scroll_x // TILE_SIZE} times",
        size=12,
        pos=(SCREEN_SIZE[0] // 2, 60),
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

                # Scroll screen to the right
                if event.key == pygame.K_RIGHT:
                    if Scrolling.scroll_x < max_scroll_x:
                        Scrolling.scroll_x += TILE_SIZE

                # Scroll screen to the left
                elif event.key == pygame.K_LEFT:
                    if Scrolling.scroll_x != 0:
                        Scrolling.scroll_x -= TILE_SIZE

                elif event.key == pygame.K_e:
                    print(export(tiles))

                # Not scrolling
                else:
                    break

                # Update scrolled text
                currently_scrolling_text = Text(
                    f"Currently scrolling {Scrolling.scroll_x} pixels ({Scrolling.scroll_x // TILE_SIZE} times out of {map_size[0]})",
                    size=12,
                    pos=(SCREEN_SIZE[0] // 2, 60),
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
        for tile in tiles:
            tile.draw(Scrolling.scroll_x, 0)
        if show_text:
            for text in texts:
                text.draw()
            currently_scrolling_text.draw()
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
