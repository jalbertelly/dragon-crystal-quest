"""Room — a rectangular grid of tiles with collision data."""

import pygame
from settings import TILE_SIZE
from world.tile import Tile, TileType, SOLID_TILES, TILE_CHAR_MAP


class Room:
    def __init__(self, width, height, generate=True):
        self.width = width    # in tiles
        self.height = height  # in tiles
        self.tiles = []
        self._wall_rects = []
        if generate:
            self._generate()

    @classmethod
    def from_layout(cls, layout_str):
        """Build a room from an ASCII layout string.

        Each character maps to a TileType via TILE_CHAR_MAP.
        """
        lines = [line for line in layout_str.strip().splitlines()]
        height = len(lines)
        width = max(len(line) for line in lines) if lines else 0

        room = cls(width, height, generate=False)
        room.tiles = []
        room._wall_rects = []

        for y, line in enumerate(lines):
            row = []
            for x in range(width):
                ch = line[x] if x < len(line) else '.'
                tile_type = TILE_CHAR_MAP.get(ch, TileType.FLOOR)
                tile = Tile(tile_type, x, y)
                if tile.is_solid:
                    room._wall_rects.append(tile.rect)
                row.append(tile)
            room.tiles.append(row)

        return room

    # -- generation (procedural test room) ---------------------------------

    def _generate(self):
        self.tiles = []
        self._wall_rects = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                if self._is_border(x, y):
                    tile = Tile(TileType.WALL, x, y)
                    self._wall_rects.append(tile.rect)
                else:
                    tile = Tile(TileType.FLOOR, x, y)
                row.append(tile)
            self.tiles.append(row)

        # Interior walls for collision testing
        self._place_wall_line(4, 5, 8, 5)
        self._place_wall_line(12, 3, 12, 8)
        self._place_wall_line(20, 10, 26, 10)
        self._place_wall_line(18, 14, 18, 19)

        self._place_wall_line(6, 12, 10, 12)
        self._place_wall_line(6, 12, 6, 16)
        self._place_wall_line(6, 16, 10, 16)

    def _is_border(self, x, y):
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1

    def _place_wall_line(self, x1, y1, x2, y2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    tile = Tile(TileType.WALL, x, y)
                    self.tiles[y][x] = tile
                    self._wall_rects.append(tile.rect)

    # -- mutations ---------------------------------------------------------

    def set_tile_type(self, grid_x, grid_y, tile_type):
        """Change a tile's type at runtime (e.g., crystal pedestal fill)."""
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            old_tile = self.tiles[grid_y][grid_x]
            new_tile = Tile(tile_type, grid_x, grid_y)
            self.tiles[grid_y][grid_x] = new_tile

            # Update wall rects
            if old_tile.rect in self._wall_rects:
                self._wall_rects.remove(old_tile.rect)
            if new_tile.is_solid:
                self._wall_rects.append(new_tile.rect)

    # -- queries ----------------------------------------------------------

    def get_wall_rects(self):
        return self._wall_rects

    def get_tile(self, grid_x, grid_y):
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.tiles[grid_y][grid_x]
        return None

    # -- rendering --------------------------------------------------------

    def draw(self, surface, camera):
        start_x = max(0, int(camera.x) // TILE_SIZE)
        start_y = max(0, int(camera.y) // TILE_SIZE)
        end_x = min(self.width, start_x + (camera.view_w // TILE_SIZE) + 2)
        end_y = min(self.height, start_y + (camera.view_h // TILE_SIZE) + 2)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.tiles[y][x].draw(surface, camera)
