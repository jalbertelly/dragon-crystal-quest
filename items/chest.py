"""Chest — treasure chest containing armor loot."""

import pygame
from settings import TILE_SIZE
from world.tile import TileType


class Chest:
    """A treasure chest placed in a dungeon room."""

    def __init__(self, grid_x, grid_y, armor_id):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.armor_id = armor_id
        self.opened = False
        self.rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE,
                                TILE_SIZE, TILE_SIZE)

    def try_open(self, interact_rect, room, game_data):
        """Attempt to open this chest.  Returns the armor name if opened."""
        if self.opened:
            return None
        if not interact_rect.colliderect(self.rect):
            return None

        self.opened = True
        room.set_tile_type(self.grid_x, self.grid_y, TileType.CHEST_OPEN)
        game_data.add_armor(self.armor_id)
        return self.armor_id
