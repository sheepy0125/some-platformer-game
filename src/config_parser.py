"""
Config parser for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

from json import load
from utils import Logger, ROOT_PATH

try:
    CONFIG_FILE_PATH = str(ROOT_PATH / "config.json")
    with open(CONFIG_FILE_PATH) as config_file:
        config_dict = load(config_file)

    SCREEN_SIZE = tuple(config_dict["screenSize"])
    FPS = int(config_dict["fps"])
    GRAVITY_MULTIPLIER = float(config_dict["gravityMultiplier"])

except Exception as error:
    Logger.log_error(error)
    exit(1)

Logger.log("Successfully loaded config")
