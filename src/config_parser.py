"""
Config parser for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

from json import load
from utils import Logger, ROOT_PATH

try:
    CONFIG_FILE_PATH = str(ROOT_PATH / "config.json")
    with open(CONFIG_FILE_PATH,'r') as config_file:
        config_dict = load(config_file)

    FPS = int(config_dict["fps"])
    GRAVITY = float(config_dict["gravity"])
    SCROLL_OFFSET = int(config_dict["scrollOffset"])

except Exception as error:
    Logger.log_error(error)
    exit(1)

del CONFIG_FILE_PATH
del config_dict
del config_file
del load

Logger.log("Successfully loaded config")
