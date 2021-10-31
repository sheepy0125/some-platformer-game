"""
Some Platformer Game
Created by duuuuck and sheepy0125
08/10/2021
"""
#############
### Setup ###
#############
# Import
from pygame_setup import pygame, screen, clock, SCROLL_OFFSET, SCREEN_SIZE
from config_parser import FPS, MAP_PATH
from entities import Player, Entity
from sounds import stop_sound
from utils import Logger, Scrolling
from world import World, load_map, get_tile_idx, snap_to_grid, TILE_SIZE

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
    map_size=(len(world.map_array[0]), len(world.map_array)),
    tile_size=TILE_SIZE,
    screen_size=SCREEN_SIZE,
)

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
    # Handle sounds
    if player.collision_types["bottom"] and abs(player.vx) > 0.1:
        world.handle_walk_sound(
            player_idx=get_tile_idx(
                snap_to_grid(player.rect.center),
                map_size=(len(world.map_array[0]), len(world.map_array)),
            )
        )
    else:
        stop_sound("grass_step")
        stop_sound("stone_step")

    # Scroll world
    Scrolling.update_scrolling(player.rect.center, SCROLL_OFFSET)

    # Draw
    screen.fill("blue")
    world.draw_tiles()
    player.draw()

    pygame.display.update()

    clock.tick(FPS)

Logger.warn("You're not supposed to see this (exited out of main loop)")
