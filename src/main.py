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
from sys import exit

# Create entities
player = Player()
entities: list[Entity] = []

while True:
    # Event handling
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT:
            running = False
            Logger.log("Shutting down gracefully")
            pygame.quit()
            exit(0)

    # Draw
    screen.fill("blue")
    player.draw()
    pygame.display.update()

Logger.warn("You're not supposed to see this (exited out of main loop)")
