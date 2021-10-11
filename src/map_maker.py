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
from pygame_setup import *
from world import Tile, load_world, TILE_SIZE
from utils import Logger, ROOT_PATH
from pygame_utils import Text

# Setup
pygame.display.set_caption("Map maker for Some Platformer Game")
tiles = []
scrolled_by = 0

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
    mouse_pos[0] += scrolled_by
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


############
### Main ###
############
texts = [
    Text("Map Maker for Some Platformer Game", size=12, pos=(SCREEN_SIZE[0] // 2, 15)),
    Text("Press H to toggle this text", size=12, pos=(SCREEN_SIZE[0] // 2, 30)),
    Text("Press the arrow keys to scroll", size=12, pos=(SCREEN_SIZE[0] // 2, 45)),
]
currently_scrolling_text = Text(
    f"Currently scrolling {scrolled_by} pixels ({scrolled_by // TILE_SIZE} times)",
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
                scrolled_by += TILE_SIZE

            # Scroll screen to the left
            elif event.key == pygame.K_LEFT:
                if scrolled_by != 0:
                    scrolled_by -= TILE_SIZE

            elif event.key == pygame.K_e:
                print(export(tiles))

            # Not scrolling
            else:
                break

            # Update scrolled text
            currently_scrolling_text = Text(
                f"Currently scrolling {scrolled_by} pixels ({scrolled_by // TILE_SIZE} times)",
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
        tile.draw(scrolled_by, 0)
    if show_text:
        for text in texts:
            text.draw()
        currently_scrolling_text.draw()
    pygame.display.update()
    clock.tick(60)
