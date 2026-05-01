"""Dungeon generator — procedural room graph builder and runtime manager."""

import random
import pygame
from settings import (
    TILE_SIZE,
    DUNGEON_ROOMS_PRE_BOSS, DUNGEON_ROOMS_POST_BOSS,
    DUNGEON_ENEMY_MIN, DUNGEON_ENEMY_MAX,
    DUNGEON_ENEMY_HARD_MIN, DUNGEON_ENEMY_HARD_MAX,
    DUNGEON_MINI_BOSS_MOBS, DUNGEON_BOSS_MOBS,
    MISSION_ARMOR, MISSION_CRYSTAL,
    THEME_VOLCANO, THEME_FROST, THEME_MARSH,
    ENEMY_DEFAULT_HP, ENEMY_DEFAULT_DAMAGE,
)
from world.room import Room
from world.tile import TileType
from world.room_templates import NORMAL_TEMPLATES, MINI_BOSS_TEMPLATE, BOSS_TEMPLATE


# ── Theme-to-hazard tile mapping ──────────────────────────────────────────

_THEME_HAZARD = {
    THEME_VOLCANO: TileType.HAZARD_LAVA,
    THEME_FROST: TileType.HAZARD_ICE,
    THEME_MARSH: TileType.HAZARD_POISON,
}


# ── Template parsing ─────────────────────────────────────────────────────

def _parse_template(layout_str, theme):
    """Pre-process a room template string.

    Extracts spawn markers and returns:
        clean_layout  – ASCII string safe for Room.from_layout()
        enemy_spawns  – list of (pixel_x, pixel_y) for enemy placement
        hazard_tiles  – list of (grid_x, grid_y) for hazard placement
        chest_candidates – list of (grid_x, grid_y) for possible chest spots
        entry_pos     – (pixel_x, pixel_y) safe player spawn (one tile inside)
        exit_tiles    – list of (grid_x, grid_y) for exit door tiles, or []
    """
    enemy_spawns = []
    hazard_tiles = []
    chest_candidates = []
    entry_tiles = []
    exit_tiles = []

    clean_lines = []
    for y, line in enumerate(layout_str.strip().splitlines()):
        clean = []
        for x, ch in enumerate(line):
            if ch == 'e':
                enemy_spawns.append((x * TILE_SIZE + 2, y * TILE_SIZE + 2))
                clean.append('.')
            elif ch == 'h':
                hazard_tiles.append((x, y))
                clean.append('.')   # placeholder — set after Room build
            elif ch == 'K':
                chest_candidates.append((x, y))
                clean.append('.')
            elif ch == '<':
                entry_tiles.append((x, y))
                clean.append('D')
            elif ch == '>':
                exit_tiles.append((x, y))
                clean.append('D')   # will be overwritten to DOOR_LOCKED
            else:
                clean.append(ch)
        clean_lines.append("".join(clean))

    clean_layout = "\n".join(clean_lines)

    # Compute safe player spawn: two tiles above the entry door so the
    # 24-px-tall sprite (1.5 tiles) doesn't overlap the bottom wall.
    if entry_tiles:
        mid_x = sum(t[0] for t in entry_tiles) / len(entry_tiles)
        entry_y = entry_tiles[0][1]
        entry_pos = (int(mid_x) * TILE_SIZE + 2, (entry_y - 2) * TILE_SIZE)
    else:
        # Fallback: centre of the room
        height = len(clean_lines)
        width = max(len(l) for l in clean_lines)
        entry_pos = ((width // 2) * TILE_SIZE, (height // 2) * TILE_SIZE)

    return (clean_layout, enemy_spawns, hazard_tiles, chest_candidates,
            entry_pos, exit_tiles)


# ── DungeonRoom ──────────────────────────────────────────────────────────

class DungeonRoom:
    """A single room inside a dungeon, wrapping a tile Room with metadata."""

    def __init__(self, room, room_type, enemy_spawns, entry_pos, exit_tiles,
                 chest=None):
        self.room = room                    # world.room.Room
        self.room_type = room_type          # "normal" | "hard" | "mini_boss" | "boss"
        self.enemy_spawns = enemy_spawns    # [(px, py), ...]
        self.entry_pos = entry_pos          # (px, py)
        self.exit_tiles = exit_tiles        # [(gx, gy), ...] or []
        self.chest = chest                  # items.chest.Chest or None
        self.cleared = False

    # -- door management ---------------------------------------------------

    def lock_exit(self):
        """Make exit door tiles solid (DOOR_LOCKED)."""
        for gx, gy in self.exit_tiles:
            self.room.set_tile_type(gx, gy, TileType.DOOR_LOCKED)

    def unlock_exit(self):
        """Make exit door tiles passable (DOOR)."""
        for gx, gy in self.exit_tiles:
            self.room.set_tile_type(gx, gy, TileType.DOOR)

    def seal_entry(self):
        """Replace entry door tiles with walls (one-way progression)."""
        # Find entry tiles (DOOR tiles on the bottom border)
        h = self.room.height
        for x in range(self.room.width):
            tile = self.room.get_tile(x, h - 1)
            if tile and tile.type == TileType.DOOR:
                self.room.set_tile_type(x, h - 1, TileType.WALL)

    def get_exit_rects(self):
        """Return list of pygame.Rects for exit door tiles."""
        return [pygame.Rect(gx * TILE_SIZE, gy * TILE_SIZE,
                            TILE_SIZE, TILE_SIZE)
                for gx, gy in self.exit_tiles]

    def get_enemy_config(self):
        """Return (hp, damage) for enemies spawned in this room."""
        if self.room_type == "mini_boss":
            return (ENEMY_DEFAULT_HP * 3, ENEMY_DEFAULT_DAMAGE * 2)
        elif self.room_type == "boss":
            return (ENEMY_DEFAULT_HP * 5, ENEMY_DEFAULT_DAMAGE * 3)
        elif self.room_type == "hard":
            return (ENEMY_DEFAULT_HP + 1, ENEMY_DEFAULT_DAMAGE)
        return (ENEMY_DEFAULT_HP, ENEMY_DEFAULT_DAMAGE)


# ── Dungeon ──────────────────────────────────────────────────────────────

class Dungeon:
    """Procedurally generated sequence of dungeon rooms for one mission."""

    def __init__(self, mission_id):
        self.mission_id = mission_id
        self.theme = {1: THEME_VOLCANO, 2: THEME_FROST, 3: THEME_MARSH}[mission_id]
        self.rooms = []                 # list[DungeonRoom]
        self.current_room_index = 0
        self._generate()

    @property
    def current_room(self):
        return self.rooms[self.current_room_index]

    @property
    def total_rooms(self):
        return len(self.rooms)

    @property
    def is_last_room(self):
        return self.current_room_index == len(self.rooms) - 1

    # -- generation --------------------------------------------------------

    def _generate(self):
        hazard_type = _THEME_HAZARD[self.theme]
        armor_id = MISSION_ARMOR[self.mission_id]

        # Room sequence:  normal×4  +  mini_boss  +  hard×3  +  boss
        sequence = []
        for _ in range(DUNGEON_ROOMS_PRE_BOSS):
            sequence.append(("normal", random.choice(NORMAL_TEMPLATES)))
        sequence.append(("mini_boss", MINI_BOSS_TEMPLATE))
        for _ in range(DUNGEON_ROOMS_POST_BOSS):
            sequence.append(("hard", random.choice(NORMAL_TEMPLATES)))
        sequence.append(("boss", BOSS_TEMPLATE))

        # Choose one normal room (0-3) for the treasure chest
        chest_room_idx = random.randint(0, DUNGEON_ROOMS_PRE_BOSS - 1)

        for idx, (room_type, template) in enumerate(sequence):
            (clean_layout, enemy_spawns, hazard_positions,
             chest_candidates, entry_pos, exit_tiles) = _parse_template(
                template, self.theme)

            room = Room.from_layout(clean_layout)

            # Set hazard tiles based on dungeon theme
            for gx, gy in hazard_positions:
                room.set_tile_type(gx, gy, hazard_type)

            # Trim enemy spawns to desired count
            enemy_spawns = self._trim_spawns(enemy_spawns, room_type)

            # Lock exit doors (if present)
            for gx, gy in exit_tiles:
                room.set_tile_type(gx, gy, TileType.DOOR_LOCKED)

            # Place chest in selected room
            chest = None
            if idx == chest_room_idx and chest_candidates:
                from items.chest import Chest
                cpos = random.choice(chest_candidates)
                room.set_tile_type(cpos[0], cpos[1], TileType.CHEST_CLOSED)
                chest = Chest(cpos[0], cpos[1], armor_id)

            droom = DungeonRoom(
                room=room,
                room_type=room_type,
                enemy_spawns=enemy_spawns,
                entry_pos=entry_pos,
                exit_tiles=exit_tiles,
                chest=chest,
            )
            self.rooms.append(droom)

    def _trim_spawns(self, spawns, room_type):
        """Randomly select a subset of enemy spawn positions."""
        random.shuffle(spawns)
        if room_type == "mini_boss":
            return spawns[:DUNGEON_MINI_BOSS_MOBS]
        elif room_type == "boss":
            return spawns[:DUNGEON_BOSS_MOBS]
        elif room_type == "hard":
            lo = min(DUNGEON_ENEMY_HARD_MIN, len(spawns))
            hi = min(DUNGEON_ENEMY_HARD_MAX, len(spawns))
            count = random.randint(lo, hi) if lo <= hi else len(spawns)
            return spawns[:count]
        else:
            lo = min(DUNGEON_ENEMY_MIN, len(spawns))
            hi = min(DUNGEON_ENEMY_MAX, len(spawns))
            count = random.randint(lo, hi) if lo <= hi else len(spawns)
            return spawns[:count]

    # -- runtime -----------------------------------------------------------

    def advance_room(self):
        """Move to the next room.  Returns the new DungeonRoom."""
        self.current_room_index += 1
        return self.current_room
