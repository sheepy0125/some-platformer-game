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
            Logger.log("Shutting down gracefully")
            pygame.quit()
            exit(0)

    player.event_handler()
    player.move(world=world)

    # Scroll world
    scroll_x += (
        player.rect.centerx - scroll_x - SCROLL_OFFSET
    ) / 10
    scroll_y += (player.rect.centery - scroll_y - 300) / 10

    # Draw
    screen.fill("blue")
    world.draw_tiles(scroll_x,scroll_y)
    player.draw(scroll_x,scroll_y)
    pygame.display.update()

    clock.tick(FPS)

Logger.warn("You're not supposed to see this (exited out of main loop)")
