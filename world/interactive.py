"""InteractiveObject — trigger zones in rooms for player interaction."""

import pygame
from enum import Enum
from settings import TILE_SIZE


class InteractType(Enum):
    BREAKFAST_TABLE = "breakfast_table"
    ARMOR_RACK = "armor_rack"
    MISSION_BOARD = "mission_board"
    CRYSTAL_PEDESTAL = "crystal_pedestal"


class InteractiveObject:
    """An interactive zone the player can activate by facing it and pressing interact."""

    def __init__(self, interact_type, grid_x, grid_y, metadata=None):
        self.type = interact_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.metadata = metadata or {}
        # Trigger rect is the tile itself
        self.rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE,
                                TILE_SIZE, TILE_SIZE)

    def __repr__(self):
        return f"InteractiveObject({self.type.value}, ({self.grid_x},{self.grid_y}))"
