import pygame
import math
from major.constants import *


def draw_gradient(surface, top_color, bottom_color):
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        color = [int(top_color[i] * (1 - ratio) + bottom_color[i] * ratio) for i in range(3)]
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))


def draw_exit_cross(surface, hovered=False):
    center = (WIDTH - 25, 25)
    length = 12
    offset = length / math.sqrt(2)
    color = (200, 0, 0) if hovered else (150, 0, 0)
    thickness = 3 if hovered else 2

    pygame.draw.line(surface, color,
                   (center[0] - offset, center[1] - offset),
                   (center[0] + offset, center[1] + offset),
                   thickness)
    pygame.draw.line(surface, color,
                   (center[0] - offset, center[1] + offset),
                   (center[0] + offset, center[1] - offset),
                   thickness)