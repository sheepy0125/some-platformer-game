"""
Map Maker for Some Platformer Game
Created by duuuuck and sheepy0125
09/10/2021
"""

#############
### Setup ###
#############
# Import
import pygame
from tkinter import Tk, Label, Button, filedialog, IntVar, Checkbutton
from tkinter.ttk import Spinbox
from tkinter.messagebox import askyesno
from world import Tile, Tiles as WorldTiles, load_map, snap_to_grid, TILE_SIZE
from pygame_utils import Text
from utils import Logger, Scrolling, ROOT_PATH
from os import system, remove
from os.path import realpath
from typing import Union

SCREEN_SIZE = (800, 800)
SIDEBAR_SIZE = (200, 800)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
DEFAULT_MAP_FILEPATH = None
TEMP_MAP_FILEPATH = str(ROOT_PATH / "src" / "maps" / "temp_map.map")

# Setup
pygame.display.set_caption("Map maker for Some Platformer Game")

###############
### Classes ###
###############
class ConfirmDialogBoxConfig:
    """
    Configuration for the confirm dialog boxes
    (at the top for easy to change)
    """

    confirm_exit = True  # Confirm exiting the program
    confirm_reset = True  # Confirm resetting the map
    confirm_run = False  # Confirm test running map


class MapSize:
    """Dataclass for map size"""

    size = (0, 0)
    resizable = False


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
        # Don't allow special tiles to be selected
        for tile_idx, tile in enumerate(tile_keys):
            if tile.startswith("_"):
                tile_keys.pop(tile_idx)

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
    def create_tile_2d_array() -> list[list]:
        tile_map = []
        # Rows
        for _ in range(MapSize.size[1]):
            # Create list of zeros
            tile_map.append([None for _ in range(MapSize.size[0])])

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

    @staticmethod
    def resize_map(new_size: tuple) -> None:
        """Resizes the map"""

        new_map = TileMap.tile_map

        # Resize columns
        # If the new size is smaller than the current size, we need to remove
        if new_size[0] < MapSize.size[0]:
            for row in new_map:
                for _ in range(MapSize.size[0] - new_size[0]):
                    row.pop()

        elif new_size[0] > MapSize.size[0]:
            for row in new_map:
                row.extend([None] * (new_size[0] - len(row)))

        # Resize rows
        # If the new size is smaller than the current size, we need to remove
        if new_size[1] < MapSize.size[1]:
            for _ in range(MapSize.size[1] - new_size[1]):
                new_map.pop()

        # If the new size is bigger than the current size, we need to add
        elif new_size[1] > MapSize.size[1]:
            for _ in range(new_size[1] - MapSize.size[1]):
                new_map.append([None for _ in range(new_size[0])])

        TileMap.tile_map = new_map


class Sidebar:
    def __init__(self):
        self.spacing = 15
        self.text_idx = 0
        self.image_size = 128

        # Background
        self.background_rect = pygame.Rect((0, 0), (SIDEBAR_SIZE[0], SIDEBAR_SIZE[1]))

        # Texts
        self.texts = [
            self.create_text("Map Maker!"),
            self.create_text("LMB: Place, RMB: Destroy"),
            self.create_text("Press the arrow keys to scroll"),
            self.create_text("Press Z to resize the map"),
            self.create_text("Press R to reset"),
            self.create_text("Press E to export"),
            self.create_text("Press I to import"),
            self.create_text("Press P to debug print the map"),
            self.create_text("Press N to switch to the next block"),
            self.create_text("Press B to switch to the prev block"),
            self.create_text("Press return to test out the map"),
            self.create_text(
                "Available tiles",
                pos=(
                    SIDEBAR_SIZE[0] // 2,
                    (self.text_idx * self.spacing) + self.image_size,
                ),
            ),
        ]
        self.create_current_tile_widgets()
        self.create_total_tiles_text()
        self.create_scroll_text()

        # Available tile texts
        self.available_tile_texts = []
        for tile_idx, (tile_id, available_tile) in enumerate(Tiles.tile_dict.items()):
            # Please note: tile_id is a string, not an int

            # Don't allow special tiles to be selected
            if tile_id.startswith("_"):
                tile_idx -= 1
                continue

            self.available_tile_texts.append(
                self.create_text(
                    f"Tile {tile_id}: {available_tile['name']}",
                    pos=(
                        SIDEBAR_SIZE[0] // 2,
                        (
                            (tile_idx * self.spacing)
                            + (self.current_tile_image_rect.bottom + self.spacing)
                        ),
                    ),
                    update_idx=False,
                )
            )

    def create_text(
        self, text: str, pos: tuple = None, update_idx: bool = True
    ) -> Text:
        """Creates a text"""

        # Create position if not provided
        if pos is None:
            pos = (SIDEBAR_SIZE[0] // 2, self.spacing * (self.text_idx + 1))

        if update_idx:
            self.text_idx += 1

        return Text(
            text_to_display=text,
            size=12,
            pos=pos,
        )

    def create_scroll_text(self):
        self.currently_scrolling_text = self.create_text(
            f"Scroll X: {Scrolling.scroll_x} | Scroll Y: {Scrolling.scroll_y}",
            pos=(
                SIDEBAR_SIZE[0] // 2,
                (self.current_tile_image_rect.top - (self.spacing * 3)),
            ),
            update_idx=False,
        )

    def create_current_tile_widgets(self):
        image_y_pos = (self.spacing * self.text_idx) + (self.spacing * 3)

        self.current_tile_text = self.create_text(
            f"Current tile: {Tiles.tile_dict[str(Tiles.current_tile)]['name']}",
            pos=(
                SIDEBAR_SIZE[0] // 2,
                image_y_pos - self.spacing,
            ),
            update_idx=False,
        )
        self.current_tile_image = pygame.transform.scale(
            pygame.image.load(Tiles.tile_dict[str(Tiles.current_tile)]["filepath"]),
            (128, 128),
        )
        self.current_tile_image_rect = self.current_tile_image.get_rect(
            centerx=(SIDEBAR_SIZE[0] // 2),
            top=image_y_pos,
        )

    def create_total_tiles_text(self):
        self.total_tiles_text = self.create_text(
            f"Total tiles: {Tiles.total_tiles}",
            pos=(SIDEBAR_SIZE[0] // 2, (SIDEBAR_SIZE[1] - (self.spacing * 2))),
            update_idx=False,
        )

    def create_size_text(self):
        self.size_text = self.create_text(
            f"{MapSize.size[0]}x{MapSize.size[1]}",
            pos=(SIDEBAR_SIZE[0] // 2, SIDEBAR_SIZE[1] - self.spacing),
            update_idx=False,
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
        self.size_text.draw()
        screen.blit(self.current_tile_image, self.current_tile_image_rect)


sidebar = Sidebar()


#################
### Functions ###
#################
def confirm_dialog(title: str, message: str) -> bool:
    """Wraps tkinter.messagebox.askyesno"""

    root = Tk()
    root.withdraw()
    answer = askyesno(title, message)
    root.update()

    return answer


def quit_handling():
    """Quits"""

    # Confirm to quit
    if ConfirmDialogBoxConfig.confirm_exit and (
        not confirm_dialog(
            "Quitting",
            "Are you SURE you want to exit? "
            "(to prevent this dialog, go to map_maker.py and set confirm_exit to False",
        )
    ):
        return

    pygame.quit()
    exit(0)


def run_map():
    """Run the map"""

    # Save the map in a temporary file
    export_map(TEMP_MAP_FILEPATH)

    # Open main.py with the temp map file as the argument
    system(f"python3 {(ROOT_PATH / 'src' / 'main.py')!s} {TEMP_MAP_FILEPATH}")

    # Remove the temp map file
    remove(TEMP_MAP_FILEPATH)


def set_max_scrolling():
    Scrolling.max_scroll_x = (MapSize.size[0] * TILE_SIZE) - (
        (SCREEN_SIZE[0] - SIDEBAR_SIZE[0]) // TILE_SIZE
    ) * TILE_SIZE
    Scrolling.max_scroll_y = (MapSize.size[1] * TILE_SIZE) - (SCREEN_SIZE[1])
    Scrolling.scroll_y = Scrolling.max_scroll_y

    Logger.log(
        f"Set up max scrolling at {Scrolling.max_scroll_x} and {Scrolling.max_scroll_y}"
    )


###########################
### Map maker functions ###
###########################
def get_tile_idx(tile_location: tuple) -> tuple:
    """
    Get the tile indecies of a tile location (top left)
    Returns a tuple with the first index being the row index and the
    second index being the column index (it's a 2D map)

    While this is pretty much a carbon copy of what is in world.py,
    we need to do a couple of things to make it work for the map maker
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


def create_tile(mouse_pos: tuple):
    tile_pos = snap_to_grid(mouse_pos)
    tile_idx = get_tile_idx(tile_pos)
    if tile_exists(tile_idx):
        return

    # Don't allow creation of tile if the max number of tiles has been reached for that tile
    if (
        max_num_of_tiles := Tiles.tile_dict[str(Tiles.current_tile)]["max_amount"]
    ) != -1 and max_num_of_tiles <= Tiles.tile_dict[str(Tiles.current_tile)]["amount"]:
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
        create_rect=False,  # We don't need to do collision, no rect needed
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


def resize_map():
    """Resizes the map"""

    if not MapSize.resizable:
        raise ValueError("The map isn't resizable!")

    # TODO: Use Tkinter instead
    # FIXME: Update total tiles

    # Get the new map size
    new_size = (
        int(input("Enter the new map  width: ")),
        int(input("Enter the new map height: ")),
    )

    # Make sure the new size is valid
    if new_size[0] < 12 or new_size[1] < 16:
        raise ValueError("The new size selected is too small!")

    elif new_size[0] < MapSize.size[0] or new_size[1] < MapSize.size[1]:
        Logger.warn("The new size selected is smaller than the current size!")
        if not confirm_dialog(
            "Resize map",
            "Are you sure you want to resize the map? This will crop the map!",
        ):
            raise ValueError("Resize aborted")

    TileMap.resize_map(new_size)

    # Update other stuff
    MapSize.size = new_size
    set_max_scrolling()
    Scrolling.scroll_x = 0
    sidebar.create_scroll_text()
    sidebar.create_total_tiles_text()
    sidebar.create_size_text()

    Logger.log("Successfully resized map")


def import_map(filepath: str = None):
    """Imports a map"""

    if filepath is None:
        # Get filepath to import from
        Tk().withdraw()
        filepath = realpath(filedialog.askopenfile().name)

    Logger.log(f"Importing map from {filepath}")

    # Set scroll x to 200. I don't know why this works, but it does.
    Scrolling.scroll_x = 200

    # Create tile map array
    tile_map_array = load_map(filepath)["map_array"]
    MapSize.size = (len(tile_map_array[0]), len(tile_map_array))
    TileMap.create_tile_2d_array()

    # Iterate through each tile in the map and update number of tiles
    for row in tile_map_array:
        for tile in row:
            # Assert tile is not NoneType
            if tile is None:
                continue

            Tiles.current_tile = tile.id
            create_tile(tile.rect.center)

    # Update other things
    Scrolling.scroll_x = 0
    set_max_scrolling()
    sidebar.create_scroll_text()
    sidebar.create_total_tiles_text()
    sidebar.create_size_text()

    Logger.log("Successfully loaded map")


def export_map(filepath: str = None):
    """Save tile to a file"""

    map_string = TileMap.convert_array_to_string()

    if filepath is None:
        # Get filepath to export to
        Tk().withdraw()
        map_file = filedialog.asksaveasfile()
        Logger.log(f"Exporting map to {map_file.name}")
    else:
        map_file = open(filepath, "w")

    with map_file:
        map_file.truncate(0)
        map_file.write(map_string)

    Logger.log("Successfully exported map")


#################
### Map setup ###
#################
def map_setup() -> tuple:
    def save_variables() -> Union[int, None]:
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
        MapSize.resizable = bool(resizable)

    root = Tk()
    root.geometry("300x200")
    root.title("Map maker setup")

    Label(root, text="Map maker setup").pack(pady=2)

    width_spinbox = Spinbox(
        root, from_=round((SCREEN_SIZE[0] - SIDEBAR_SIZE[0]) / TILE_SIZE), to=500
    )
    height_spinbox = Spinbox(root, from_=round(SCREEN_SIZE[1] // TILE_SIZE), to=500)

    resizable = IntVar()
    resizable.set(0)
    resizable_checkbox = Checkbutton(
        root, text="Resizable", variable=resizable, onvalue=1, offvalue=0
    )

    Label(root, text="Width").pack(pady=2)
    width_spinbox.pack(pady=2)
    Label(root, text="Height").pack(pady=2)
    height_spinbox.pack(pady=2)
    resizable_checkbox.pack(pady=2)

    Button(root, text="Go!", command=save_variables).pack(pady=2)

    root.mainloop()

    Logger.log(f"Map size is {MapSize.size}")
    return MapSize.size


############
### Main ###
############
def main():
    # Setup
    map_setup()
    set_max_scrolling()
    sidebar.create_size_text()
    TileMap.create_tile_2d_array()

    # Main loop
    while True:
        # Event handler
        for event in pygame.event.get():
            # Quitting
            if event.type == pygame.QUIT:
                quit_handling()

            # Keypress
            if event.type == pygame.KEYUP:
                # Resize map
                if event.key == pygame.K_x:
                    try:
                        resize_map()
                    except Exception as error:
                        Logger.fatal("Failed to resize map")
                        Logger.log_error(error)

                # Reset map
                elif event.key == pygame.K_r:
                    # Confirm
                    if ConfirmDialogBoxConfig.confirm_reset and (
                        not confirm_dialog(
                            "Resetting map",
                            "Are you SURE you want to reset the map? "
                            "(to disable this message, go into map_maker.py "
                            "and set confirm_reset to False)",
                        )
                    ):
                        break
                    # Reset tile map
                    TileMap.create_tile_2d_array()
                    Tiles.total_tiles = 0
                    for tile_id in Tiles.tile_dict:
                        Tiles.tile_dict[tile_id]["amount"] = 0
                    # Reset sidebar
                    sidebar.create_total_tiles_text()

                # Debug print
                elif event.key == pygame.K_p:
                    TileMap.debug_print()

                # Test run map
                elif event.key == pygame.K_RETURN:
                    # Confirm
                    if ConfirmDialogBoxConfig.confirm_run and (
                        not confirm_dialog(
                            "Running map",
                            "Are you SURE you want to run the map? "
                            "(to disable this message, go into map_maker.py and "
                            "set confirm_run to False)",
                        )
                    ):
                        break

                    # Run map
                    try:
                        run_map()
                    except Exception as error:
                        Logger.fatal("Failed to test run map")
                        Logger.log_error(error)

                # Export
                elif event.key == pygame.K_e:
                    try:
                        export_map()
                    except Exception as error:
                        Logger.fatal("Failed to export map")
                        Logger.log_error(error)

                # Import
                elif event.key == pygame.K_i:
                    try:
                        import_map()
                    except Exception as error:
                        Logger.fatal("Failed to import map")
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
                    if Scrolling.scroll_x < Scrolling.max_scroll_x:
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
                    if Scrolling.scroll_y < Scrolling.max_scroll_y:
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
                    tile.draw(optimize=False)

        sidebar.draw()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
