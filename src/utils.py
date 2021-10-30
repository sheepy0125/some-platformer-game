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
        Scrolling.max_scroll_y = (map_size[1] * tile_size) - (screen_size[1])

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
