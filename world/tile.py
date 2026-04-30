"""Tile — a single cell in the world grid."""

import pygame
from enum import Enum
from settings import (
    TILE_SIZE, FLOOR_COLOR, FLOOR_COLOR_ALT,
    WALL_COLOR, WALL_HIGHLIGHT, DARK_GRAY,
    CARPET_COLOR, CARPET_COLOR_ALT,
    DOOR_COLOR, DOOR_FRAME_COLOR,
    PEDESTAL_COLOR, PEDESTAL_GLOW_RED, PEDESTAL_GLOW_BLUE, PEDESTAL_GLOW_GREEN,
    TABLE_COLOR, FOOD_COLOR,
    ARMOR_RACK_COLOR, BOARD_COLOR, BANNER_COLOR, TORCH_COLOR,
    WHITE,
)


class TileType(Enum):
    FLOOR = 0
    WALL = 1
    CARPET = 2
    DOOR = 3
    PEDESTAL_EMPTY = 4
    PEDESTAL_RED = 5
    PEDESTAL_BLUE = 6
    PEDESTAL_GREEN = 7
    TABLE = 8
    ARMOR_RACK = 9
    MISSION_BOARD = 10
    BANNER = 11
    TORCH = 12

# Tile types that block movement
SOLID_TILES = {
    TileType.WALL, TileType.TABLE,
    TileType.ARMOR_RACK, TileType.MISSION_BOARD,
    TileType.BANNER, TileType.PEDESTAL_EMPTY,
    TileType.PEDESTAL_RED, TileType.PEDESTAL_BLUE, TileType.PEDESTAL_GREEN,
}

# Single-char codes for ASCII room layouts
TILE_CHAR_MAP = {
    '.': TileType.FLOOR,
    '#': TileType.WALL,
    'c': TileType.CARPET,
    'D': TileType.DOOR,
    'p': TileType.PEDESTAL_EMPTY,
    'R': TileType.PEDESTAL_RED,
    'B': TileType.PEDESTAL_BLUE,
    'G': TileType.PEDESTAL_GREEN,
    'T': TileType.TABLE,
    'A': TileType.ARMOR_RACK,
    'M': TileType.MISSION_BOARD,
    'b': TileType.BANNER,
    't': TileType.TORCH,
}


class Tile:
    def __init__(self, tile_type, grid_x, grid_y):
        self.type = tile_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(grid_x * TILE_SIZE,
                                grid_y * TILE_SIZE,
                                TILE_SIZE, TILE_SIZE)

    @property
    def is_solid(self):
        return self.type in SOLID_TILES

    def draw(self, surface, camera):
        draw_rect = camera.apply(self.rect)
        x, y = draw_rect.x, draw_rect.y
        s = TILE_SIZE

        if self.type == TileType.FLOOR:
            alt = (self.grid_x + self.grid_y) % 2 == 0
            color = FLOOR_COLOR if alt else FLOOR_COLOR_ALT
            pygame.draw.rect(surface, color, draw_rect)

        elif self.type == TileType.WALL:
            pygame.draw.rect(surface, WALL_COLOR, draw_rect)
            pygame.draw.rect(surface, WALL_HIGHLIGHT, draw_rect, 1)
            mid_y = y + s // 2
            pygame.draw.line(surface, DARK_GRAY,
                             (x, mid_y), (x + s, mid_y))

        elif self.type == TileType.CARPET:
            alt = (self.grid_x + self.grid_y) % 2 == 0
            color = CARPET_COLOR if alt else CARPET_COLOR_ALT
            pygame.draw.rect(surface, color, draw_rect)

        elif self.type == TileType.DOOR:
            pygame.draw.rect(surface, DOOR_COLOR, draw_rect)
            # Door frame edges
            pygame.draw.rect(surface, DOOR_FRAME_COLOR, draw_rect, 2)

        elif self.type in (TileType.PEDESTAL_EMPTY, TileType.PEDESTAL_RED,
                           TileType.PEDESTAL_BLUE, TileType.PEDESTAL_GREEN):
            # Floor underneath
            pygame.draw.rect(surface, FLOOR_COLOR, draw_rect)
            # Pedestal base
            base = pygame.Rect(x + 2, y + 4, s - 4, s - 4)
            pygame.draw.rect(surface, PEDESTAL_COLOR, base)
            pygame.draw.rect(surface, WHITE, base, 1)
            # Crystal glow if filled
            glow_map = {
                TileType.PEDESTAL_RED: PEDESTAL_GLOW_RED,
                TileType.PEDESTAL_BLUE: PEDESTAL_GLOW_BLUE,
                TileType.PEDESTAL_GREEN: PEDESTAL_GLOW_GREEN,
            }
            if self.type in glow_map:
                gem = pygame.Rect(x + 5, y + 2, s - 10, s - 8)
                pygame.draw.rect(surface, glow_map[self.type], gem)

        elif self.type == TileType.TABLE:
            pygame.draw.rect(surface, FLOOR_COLOR, draw_rect)
            table = pygame.Rect(x + 1, y + 2, s - 2, s - 3)
            pygame.draw.rect(surface, TABLE_COLOR, table)
            # Food on table
            pygame.draw.rect(surface, FOOD_COLOR,
                             pygame.Rect(x + 4, y + 4, 4, 3))
            pygame.draw.rect(surface, FOOD_COLOR,
                             pygame.Rect(x + 9, y + 5, 3, 3))

        elif self.type == TileType.ARMOR_RACK:
            pygame.draw.rect(surface, FLOOR_COLOR, draw_rect)
            # Rack frame
            pygame.draw.rect(surface, ARMOR_RACK_COLOR,
                             pygame.Rect(x + 2, y + 1, s - 4, s - 1))
            # Armor silhouette
            pygame.draw.rect(surface, WALL_HIGHLIGHT,
                             pygame.Rect(x + 5, y + 3, s - 10, s - 6))

        elif self.type == TileType.MISSION_BOARD:
            pygame.draw.rect(surface, WALL_COLOR, draw_rect)
            # Board
            board = pygame.Rect(x + 2, y + 2, s - 4, s - 4)
            pygame.draw.rect(surface, BOARD_COLOR, board)
            pygame.draw.rect(surface, TABLE_COLOR, board, 1)

        elif self.type == TileType.BANNER:
            pygame.draw.rect(surface, WALL_COLOR, draw_rect)
            # Banner hanging
            pygame.draw.rect(surface, BANNER_COLOR,
                             pygame.Rect(x + 4, y + 2, s - 8, s - 3))

        elif self.type == TileType.TORCH:
            pygame.draw.rect(surface, WALL_COLOR, draw_rect)
            # Torch flame
            pygame.draw.rect(surface, TORCH_COLOR,
                             pygame.Rect(x + 6, y + 3, 4, 5))
            pygame.draw.rect(surface, WHITE,
                             pygame.Rect(x + 7, y + 4, 2, 3))
