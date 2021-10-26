"""
Some Platformer Game
Created by duuuuck and sheepy0125
08/10/2021
"""
#############
### Setup ###
#############

from pygame_setup import pygame, screen, clock, SCROLL_OFFSET
from config_parser import FPS, MAP_PATH
from entities import Player, Entity
from utils import Logger, Scrolling, ROOT_PATH
from world import World, load_map

# Create world
map_data = load_map(MAP_PATH)
world = World(map_array=map_data["map_array"], player_pos=map_data["player_pos"])

# Create entities
player = Player(world.player_pos)
entities: list[Entity] = []


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
        player.rect.centerx - Scrolling.scroll_x - SCROLL_OFFSET[0]
    ) / 10
    Scrolling.scroll_y += (
        player.rect.centery - Scrolling.scroll_y - SCROLL_OFFSET[1]
    ) / 10

    # Draw
    screen.fill("blue")
    world.draw_tiles()
    player.draw()
    pygame.display.update()

    clock.tick(FPS)

Logger.warn("You're not supposed to see this (exited out of main loop)")
