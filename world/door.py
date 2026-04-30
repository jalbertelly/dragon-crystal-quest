"""Door — a transition point connecting two rooms."""

import pygame
from settings import TILE_SIZE


class Door:
    """Represents a door connecting two rooms in the castle."""

    def __init__(self, grid_x, grid_y, target_room, spawn_name):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.target_room = target_room
        self.spawn_name = spawn_name  # named spawn point in the target room
        self.rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE,
                                TILE_SIZE, TILE_SIZE)
