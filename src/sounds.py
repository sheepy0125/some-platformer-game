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

    sound_dict = {
        "jump": {"filename": str(SOUND_PATH / "jump.wav"), "idx": 0},
        "grass_step": {"filename": str(SOUND_PATH / "grass_step.wav"), "idx": 1},
        "stone_step": {"filename": str(SOUND_PATH / "stone_step.wav"), "idx": 2},
        "damage": {"filename": str(SOUND_PATH / "damage.wav"), "idx": 3},
        "death": {"filename": str(SOUND_PATH / "death.wav"), "idx": 4},
    }


# Initialize sounds
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=(2 ** 12))
channels = [pygame.mixer.Channel(i) for i in range(len(Sounds.sound_dict))]


##################
### Play sound ###
##################
def play_sound(sound_name: str, volume: float = 1.0):
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
        channels[sound_idx].set_volume(volume)
        channels[sound_idx].play(sound)
    except KeyError:
        Logger.fatal(f"Sound {sound_name} not found, cannot play")
    except RuntimeError:
        # This occurs when the sound is already being played.
        # Logger.log("Attempted to play sound, but the sound is already playing")
        pass
    except Exception as error:
        Logger.fatal(
            "Error in playing sound: Sound was found, but another error occurred"
        )
        Logger.log_error(error)


##################
### Stop sound ###
##################
def stop_sound(sound_name: str):
    try:
        sound_idx = Sounds.sound_dict[sound_name]["idx"]
        channels[sound_idx].stop()
    except KeyError:
        Logger.fatal(f"Sound {sound_name} not found, cannot stop")
    except Exception as error:
        Logger.fatal(
            "Error in stopping sound: Sound was found, but another error occurred"
        )
        Logger.log_error(error)
