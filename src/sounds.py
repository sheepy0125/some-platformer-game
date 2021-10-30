"""
Handles sounds for Some Platformer Game
Created by sheepy0125
30/10/2021
"""

#############
### Setup ###
#############
# Import
from pygame_setup import pygame
from utils import Logger, ROOT_PATH
from time import time

# Variables
SOUND_PATH = ROOT_PATH / "assets" / "sfx"

#######################
### Sound dataclass ###
#######################
class Sounds:
    """Dataclass for storing sounds"""

    # Note: the duration isn't needed but it is nice to have
    sound_dict = {
        "jump": {"filename": str(SOUND_PATH / "jump.wav"), "duration": 0.19, "idx": 0},
        "step": {"filename": str(SOUND_PATH / "step.wav"), "duration": 0.17, "idx": 1},
        "damage": {
            "filename": str(SOUND_PATH / "damage.wav"),
            "duration": 2.8,
            "idx": 2,
        },
        "death": {"filename": str(SOUND_PATH / "death.wav"), "duration": 0.4, "idx": 3},
    }


# Initialize sounds
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=(2 ** 12))
channels = [pygame.mixer.Channel(i) for i in range(len(Sounds.sound_dict))]


##################
### Play sound ###
##################
def play_sound(sound_name: str):
    """
    Plays a sound with error handling
    Has timeouts as well
    Refer to Sounds.sound_dict for sound names
    """

    try:
        sound = pygame.mixer.Sound(Sounds.sound_dict[sound_name]["filename"])
        sound_idx = Sounds.sound_dict[sound_name]["idx"]

        # Ensure sound is not already playing
        if channels[sound_idx].get_busy():
            raise RuntimeError

        # Play sound
        channels[sound_idx].play(sound)
    except KeyError:
        Logger.fatal(f"Sound {sound_name} not found, cannot play")
    except RuntimeError:
        # This occurs when the sound is already being played.
        Logger.log("Attempted to play sound, but the sound is already playing")
    except Exception as error:
        Logger.fatal("Sound was found, but another error occurred")
        Logger.log_error(error)
