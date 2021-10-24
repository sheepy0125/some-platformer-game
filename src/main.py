"""
Some Platformer Game
Created by duuuck and sheepy0125
08/10/2021
"""
#############
### Setup ###
#############

from pygame_setup import pygame, screen, clock
from config_parser import SCROLL_OFFSET, FPS
from entities import Player, Entity
from utils import Logger, Scrolling, ROOT_PATH
from world import World, load_world

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
    Scrolling.scroll_x += (
        player.rect.centerx - Scrolling.scroll_x - SCROLL_OFFSET
    ) / 10
    Scrolling.scroll_y += (player.rect.centery - Scrolling.scroll_y - 300) / 10

    # Draw
    screen.fill("blue")
    world.draw_tiles()
    player.draw()
    pygame.display.update()

    clock.tick(FPS)

Logger.warn("You're not supposed to see this (exited out of main loop)")
