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
