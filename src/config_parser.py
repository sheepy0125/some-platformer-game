"""
Config parser for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

from json import load
from utils import Logger
from pathlib import Path

try:
    CONFIG_FILE_PATH = str(Path(__file__).parent.parent / "config.json")
    with open(CONFIG_FILE_PATH) as config_file:
        config_dict = load(config_file)

    SCREEN_SIZE = tuple(config_dict["screenSize"])

except Exception as error:
    Logger.log_error(error)
    exit(1)

Logger.log("Successfully loaded config")
