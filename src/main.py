"""
Some Platformer Game
Created by duuuuck and sheepy0125
08/10/2021
"""
#############
### Setup ###
#############

from pygame_setup import pygame, screen, clock, SCROLL_OFFSET, SCREEN_SIZE
from config_parser import FPS, MAP_PATH
from entities import Player, Entity
from utils import Logger, Scrolling
from world import World, load_map, TILE_SIZE

from time import time

# Create world
map_data = load_map(MAP_PATH)
world = World(
    map_array=map_data["map_array"],
    player_pos=map_data["player_pos"],
    end_tile_pos=map_data["end_tile"],
)

# Create entities
player = Player(world.player_pos)
entities: list[Entity] = []


# Setup scrolling
Scrolling.setup_scrolling(
    map_size=(len(world.map_array), len(world.map_array[0])),
    tile_size=TILE_SIZE,
    screen_size=SCREEN_SIZE,
)
d = time()
while True:
    if time() - d > 0.165:
        print(1 / (time() - d))
    d = time()
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
    Scrolling.update_scrolling(player.rect.center, SCROLL_OFFSET)

    # Draw
    screen.fill("blue")
    world.draw_tiles()
    player.draw()

    pygame.display.update()

    clock.tick(FPS)

Logger.warn("You're not supposed to see this (exited out of main loop)")
