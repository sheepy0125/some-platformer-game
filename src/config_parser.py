"""
Config parser for Some Platformer Game
Created by sheepy0125
08/10/2021
"""

from json import load
from utils import Logger, ROOT_PATH
from sys import argv

try:
    CONFIG_FILE_PATH = str(ROOT_PATH / "config.json")
    with open(CONFIG_FILE_PATH, "r") as config_file:
        config_dict = load(config_file)

    FPS = int(config_dict["fps"])
    GRAVITY = float(config_dict["gravity"])

    # Get the first map to play if it is in the env
    MAP_PATH = ROOT_PATH / "src" / "maps"
    if len(argv) > 1:
        MAP_PATH /= argv[1]
    else:
        MAP_PATH /= "0-test.map"
    MAP_PATH = str(MAP_PATH)


except Exception as error:
    Logger.log_error(error)
    exit(1)

del CONFIG_FILE_PATH
del config_dict
del config_file
del load
del argv

Logger.log("Successfully loaded config")
