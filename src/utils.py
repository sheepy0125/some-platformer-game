"""
Tools for Some Platformer Game
Created by sheepy0125
02/10/2021
"""

from pathlib import Path

###############
### Globals ###
###############
ROOT_PATH: Path = Path(__file__).parent.parent

####################
### Logger class ###
####################
class Logger:
    """Log messages with ease"""

    colors: dict = {
        "log": "\033[92m",
        "warn": "\033[93m",
        "fatal": "\033[91m",
        "normal": "\033[0m",
    }

    @staticmethod
    def log(message: str):
        print(f"{Logger.colors['log']}[INFO] {message}{Logger.colors['normal']}")

    @staticmethod
    def warn(message: str):
        print(f"{Logger.colors['warn']}[WARN] {message}{Logger.colors['normal']}")

    @staticmethod
    def fatal(message: str):
        print(f"{Logger.colors['fatal']}[FAIL] {message}{Logger.colors['normal']}")

    @staticmethod
    def log_error(error: Exception):
        Logger.fatal(
            f"{type(error).__name__}: {str(error)} (line {error.__traceback__.tb_lineno})"
        )


#############################
### Scroll handling class ###
#############################
class Scrolling:
    scroll_x: float = 0
    scroll_y: float = 0
    max_scroll_x: float = 0
    max_scroll_y: float = 0

    @staticmethod
    def setup_scrolling(map_size, tile_size, screen_size):
        """Setup scrolling"""

        Scrolling.max_scroll_x = (map_size[0] * tile_size) - (screen_size[0])
        Scrolling.max_scroll_y = (map_size[1] * tile_size) - (screen_size[1]) - 50

        Logger.log(
            f"Max scrolling: ({Scrolling.max_scroll_x}, {Scrolling.max_scroll_y})"
        )

    @staticmethod
    def update_scrolling(player_pos, scroll_offset):
        """Update scrolling"""

        # Center player
        Scrolling.scroll_x += (
            player_pos[0] - Scrolling.scroll_x - scroll_offset[0]
        ) / 10
        Scrolling.scroll_y += (
            player_pos[1] - Scrolling.scroll_y - scroll_offset[1]
        ) / 10

        # Don't allow scrolling off the map

        # X axis
        if Scrolling.scroll_x <= 0:
            Scrolling.scroll_x = 0
        elif Scrolling.scroll_x >= Scrolling.max_scroll_x:
            Scrolling.scroll_x = Scrolling.max_scroll_x

        # Y axis
        if Scrolling.scroll_y <= 0:
            Scrolling.scroll_y = 0
        elif Scrolling.scroll_y >= Scrolling.max_scroll_y:
            Scrolling.scroll_y = Scrolling.max_scroll_y

class Animations:

    def __init__(self,image_path,cols,rows,dict_names):
        self.sprites = self.get_images_from_spritesheet(image_path,cols,rows)
        self.dict = self.load_dict(dict_names)
    def load_dict(self,dict_names):
        for i in range(len(sprites)):
            self.dict[dict_names[i]] = sprites[i]

    def add_extra_sprites(self):
        for i in self.dict:
            copied_sprites = self.dict[i].copy()
            squashed_sprites = []
            stretched_sprites = []
            for i in copied_sprites:
                squashed_sprite = pygame.transform.scale()
                squashed_sprites.append()
                stretched_sprites.append()



    def get_images_from_spritesheet(image_path, cols, rows):
        """ 
            get the images from the spritesheet
            cols is number of columns
            rows is number of rows
        """
        spritesheet = pygame.image.load(image_path)
        sprite_width = spritesheet.get_width() / cols
        sprite_height = spritesheet.get_height() / rows

        empty_image = pygame.Surface((sprite_width,sprite_height)).get_buffer().raw

        rows = []

        # loop through the number of columns
        for col_num in range(cols):
            # get the x position of the sprite by multiplying 
            # the column that its on by the width
            
            x_pos = col_num * sprite_width
            row_images = []
            for row_num in range(rows):
                # loop through the number of rows
                y_pos = row_num * sprite_height
                sprite_rect = (x_pos, y_pos, sprite_width, sprite_height)
                sprite = spritesheet.subsurface(sprite_rect)
                if sprite.get_buffer().raw == empty_image:
                    continue
                row_images.append(sprite)

            rows.append(row_images)

        return rows
