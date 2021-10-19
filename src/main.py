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

from time import time

# Create entities
player = Player()
entities: list[Entity] = []
frame = time()

# Create world
world = World(load_world(str(ROOT_PATH / "src" / "maps" / "0-test.map")))

while True:
    time_elapsed = time() - frame
    frame = time()

    # Event handling
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            Logger.log("Shutting down gracefully")
            pygame.quit()
            exit(0)

    player.event_handler()
    player.move(time_elapsed = time_elapsed,world=world)
    # Scroll world
    Scrolling.scroll_x += (
        player.rect.centerx - Scrolling.scroll_x - SCROLL_OFFSET
    ) / 10 * (60 * time_elapsed)
    Scrolling.scroll_y += (player.rect.centery - Scrolling.scroll_y - 300) / 10 * (time_elapsed * 60)
        # Draw

    print(player.vy)

    screen.fill("blue")
    world.draw_tiles()
    player.draw()
    pygame.display.update()

Logger.warn("You're not supposed to see this (exited out of main loop)")
