import pygame
import sys

SCREENSIZE = (500, 500)

screen = pygame.display.set_mode(SCREENSIZE)

TILESIZE = 32

rects = []


def snap_to_grid(location):
    new_location = list(location)
    new_location[0] = int(location[0] / TILESIZE) * TILESIZE
    new_location[1] = int(location[1] / TILESIZE) * TILESIZE

    return new_location


def new_rect(mouse_loc):
    mx, my = mouse_loc
    return pygame.Rect(snap_to_grid((mx, my)), (TILESIZE, TILESIZE))


def export():
    pass


while True:
    print(snap_to_grid((0, 100))[1] / TILESIZE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rects.append(new_rect(pygame.mouse.get_pos()))

    pygame.draw.rect(screen, (255, 255, 255), new_rect(pygame.mouse.get_pos()))

    for rect in rects:
        pygame.draw.rect(screen, (255, 255, 255), rect)

    pygame.display.update()
    screen.fill((0, 0, 0))
