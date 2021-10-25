import pygame

from utils import Logger, ROOT_PATH

from tkinter import filedialog, Tk

Tk().withdraw()

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

offset = [0, 0]

TILE_SIZE = 50

player = pygame.image.load(
    str(ROOT_PATH / "assets" / "images" / "tiles" / "player.png")
)
dirt = pygame.image.load(str(ROOT_PATH / "assets" / "images" / "tiles" / "dirt.png"))
dirt = pygame.transform.scale(dirt, (TILE_SIZE, TILE_SIZE))

tile_mode = 1

game_map = {}


def snap_to_grid(mouse_pos: tuple) -> tuple:
    """Returns the top left coordinate of a tile from a mouse position"""

    return tuple(
        [((mouse_pos[i] + offset[i]) // TILE_SIZE) * TILE_SIZE for i in range(2)]
    )


def save_to_file(msg):
    """Saves msg to the file the user selects"""
    file = filedialog.asksaveasfile(
        initialdir="C:\\Users\\ryden\\some-platformer-game\\src\\maps",
        defaultextension=".map",
        filetypes=[("MAP file", ".map"), ("All files", ".*")],
    )
    if file == None:
        return
    file.write(msg)
    file.close()


def open_file():
    """Returns contents of the file the user selects"""
    file = filedialog.askopenfile(
        initialdir="C:\\Users\\ryden\\some-platformer-game\\src\\maps",
        defaultextension=".map",
        filetypes=[("MAP file", ".map"), ("All files", ".*")],
    )

    if file == None:
        return
    msg = file.read()
    file.close()
    return msg


def export():
    # TODO : write docstring

    tile_map = {}

    min_pos = [10000, 10000]
    max_pos = [-10000, -10000]
    for tile in game_map:
        grid = tile
        tile = list(tile)
        tile[0] = tile[1] // TILE_SIZE
        tile[1] = tile[0] // TILE_SIZE
        min_pos[0] = min(tile[0], min_pos[0])
        min_pos[1] = min(tile[1], min_pos[1])
        max_pos[0] = max(tile[0], max_pos[0])
        max_pos[1] = max(tile[1], max_pos[1])
        tile = tuple(tile)
        tile_map[tile] = game_map[grid]

    grid_size = [max_pos[0] - min_pos[0] + 1, max_pos[1] - min_pos[1] + 1]

    tile_map1 = {}

    for tile in tile_map:
        n = tile_map[tile]
        tile = list(tile)
        tile[0] -= min_pos[0]
        tile[1] -= min_pos[1]
        tile = tuple(tile)
        tile_map1[tile] = n

    tile_map = tile_map1
    del tile_map1
    new_grid = []

    for i in range(grid_size[0]):
        layer = []
        for j in range(grid_size[1]):
            if (i, j) in tile_map:
                layer.append(tile_map[(i, j)])
            else:
                layer.append(0)
        new_grid.append(layer)

    grid = ""

    for i in range(len(new_grid)):
        for j in range(len(new_grid[0])):
            grid += str(new_grid[i][j])
        grid += "\n"

    save_to_file(grid)


while True:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                export()

    if pygame.mouse.get_pressed()[0]:
        game_map[snap_to_grid(pygame.mouse.get_pos())] = tile_mode
    if pygame.mouse.get_pressed()[2]:
        if snap_to_grid(pygame.mouse.get_pos()) in game_map:
            del game_map[snap_to_grid(pygame.mouse.get_pos())]

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        offset[0] -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        offset[0] += 5
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        offset[1] -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        offset[1] += 5

    for key in game_map:
        key = list(key)
        key[0] -= offset[0]
        key[1] -= offset[1]
        screen.blit(dirt, key)

    pygame.display.update()
    screen.fill("blue")
