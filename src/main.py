"""
Some Platformer Game
Created by duuuck and sheepy0125
08/10/2021
"""

#############
### Setup ###
#############
# Import
from pygame_setup import *
from entities import *
from utils import Logger, ROOT_PATH
from world import *
from sys import exit

# Create entities
player = Player()
entities: list[Entity] = []

# Create world
world = World(load_world(str(ROOT_PATH / "src" / "maps" / "0-test.map")))

while True:
    # Event handling
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            running = False
            Logger.log("Shutting down gracefully")
            pygame.quit()
            exit(0)

    player.movement_handler()

    # Draw
    screen.fill("blue")
    world.draw_tiles()
    player.draw()
    pygame.display.update()
    clock.tick(FPS)

Logger.warn("You're not supposed to see this (exited out of main loop)")
