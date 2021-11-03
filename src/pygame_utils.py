"""
Pygame utils for Some Platformer Game
Created by sheepy0125
10/10/2021
"""

from pygame_setup import pygame, screen
from typing import Union

pygame.font.init()


class Text:
    """Display text for Pygame"""

    def __init__(
        self,
        text_to_display: str,
        pos: tuple,
        size: int,
        color: Union[str, tuple] = "white",
    ):
        # Create text
        self.text_surf = pygame.font.SysFont("Arial", size).render(
            text_to_display, True, color
        )
        self.text_rect = self.text_surf.get_rect(center=pos)

    def draw(self):
        screen.blit(self.text_surf, self.text_rect)


class Button:
    """Display a button for Pygame"""

    def __init__(self, pos: tuple, size: tuple, color: Union[str, tuple] = "white"):
        self.button_pos = pos
        self.button_size = size
        self.button_color = color

        self.button_rect = CenterRect(
            pos=self.button_pos, size=self.button_size, color=self.button_color
        )

        # Cooldown stuff
        self.button_cooldown_time_over = 0
        self.button_cooldown_time_ms = 100

    def check_pressed(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        cooldown_over = self.button_cooldown_time_over <= pygame.time.get_ticks()

        if (
            self.button_rect.rect.collidepoint(mouse_pos)
            and mouse_click[0]
            and cooldown_over
        ):
            self.button_cooldown_time_over = (
                pygame.time.get_ticks() + self.button_cooldown_time_ms
            )

            return True

        return False

    def draw(self):
        self.button_rect.draw()


class CenterRect:
    """A Pygame rectangle, but it is centered. Don't ask"""

    def __init__(self, pos: tuple, size: tuple, color: Union[str, tuple] = "white"):
        self.center_pos = pos
        self.size = size
        self.color = color

        # Get center position -> left / top positions
        self.left = self.center_pos[0] - (self.size[0] * 0.5)
        self.top = self.center_pos[1] - (self.size[1] * 0.5)

        # Create rectangle
        self.rect = pygame.Rect(self.left, self.top, *self.size)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
