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
from sys import exit

# Create entities
player = Player()
entities: list[Entity] = []

x_offset = 0

while True:
    x_offset -= (player.rect.centerx - SCREEN_SIZE[0]/2 + x_offset)/10
    # Event handling
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            running = False
            Logger.log("Shutting down gracefully")
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_SPACE:
                pass
                # enter jump here

    player.movement_handler()

    # Draw
    screen.fill("blue")
    player.draw(x_offset)
    pygame.display.update()
    clock.tick(FPS)

Logger.warn("You're not supposed to see this (exited out of main loop)")
