"""Castle — the Dragon Castle hub world with multiple handcrafted rooms."""

from world.room import Room
from world.door import Door
from world.interactive import InteractiveObject, InteractType
from world.tile import TileType
from settings import TILE_SIZE

# ── Room layout legend ──────────────────────────────────────────────
#   # = wall       . = floor      c = carpet     D = door
#   p = pedestal   T = table      A = armor rack  M = mission board
#   b = banner     t = torch
# ────────────────────────────────────────────────────────────────────

MAIN_HALL_LAYOUT = """\
####################
#t.b..p.M.p.M.p.b.t#
#..................#
#..................#
#..................#
#..................#
#..cccccccccccc....#
#..cccccccccccc....#
#..cccccccccccc....#
#..................#
D..................D
#..................#
#..................#
#......cccc........#
#......cccc........#
####################"""

BREAKFAST_HALL_LAYOUT = """\
##############
#t.b......b.t#
#............#
#..TTTTTT....#
#..TTTTTT....#
#............#
#............#
#............#
#............#
#......b.....#
#t...........D
##############"""

ARMORY_LAYOUT = """\
##############
#t.AAAA..AA.t#
#............#
#............#
#A..........A#
#A..........A#
#............#
#............#
#............#
#.b......b...#
D...........t#
##############"""

# Named spawn points: {room_name: {spawn_name: (grid_x, grid_y)}}
SPAWN_POINTS = {
    "main_hall": {
        "from_breakfast": (2, 10),
        "from_armory": (17, 10),
        "default": (9, 8),
    },
    "breakfast_hall": {
        "from_main": (11, 10),
        "default": (6, 6),
    },
    "armory": {
        "from_main": (2, 10),
        "default": (6, 6),
    },
}

# Door definitions: (grid_x, grid_y, target_room, spawn_name_in_target)
DOOR_DEFS = {
    "main_hall": [
        Door(0, 10, "breakfast_hall", "from_main"),
        Door(19, 10, "armory", "from_main"),
    ],
    "breakfast_hall": [
        Door(13, 10, "main_hall", "from_breakfast"),
    ],
    "armory": [
        Door(0, 10, "main_hall", "from_armory"),
    ],
}

# Interactive object definitions per room
INTERACTIVE_DEFS = {
    "main_hall": [
        # Crystal pedestals (positions match 'p' chars in layout row 1)
        InteractiveObject(InteractType.CRYSTAL_PEDESTAL, 6, 1,
                          {"crystal": "red"}),
        InteractiveObject(InteractType.CRYSTAL_PEDESTAL, 10, 1,
                          {"crystal": "blue"}),
        InteractiveObject(InteractType.CRYSTAL_PEDESTAL, 14, 1,
                          {"crystal": "green"}),
        # Mission boards (positions match 'M' chars in layout row 1)
        InteractiveObject(InteractType.MISSION_BOARD, 8, 1),
        InteractiveObject(InteractType.MISSION_BOARD, 12, 1),
    ],
    "breakfast_hall": [
        # Table tiles the player can face and interact with
        InteractiveObject(InteractType.BREAKFAST_TABLE, 4, 3),
        InteractiveObject(InteractType.BREAKFAST_TABLE, 5, 3),
        InteractiveObject(InteractType.BREAKFAST_TABLE, 6, 3),
        InteractiveObject(InteractType.BREAKFAST_TABLE, 7, 3),
    ],
    "armory": [
        # Top-row armor racks (row 1)
        InteractiveObject(InteractType.ARMOR_RACK, 3, 1),
        InteractiveObject(InteractType.ARMOR_RACK, 4, 1),
        InteractiveObject(InteractType.ARMOR_RACK, 5, 1),
        InteractiveObject(InteractType.ARMOR_RACK, 6, 1),
        InteractiveObject(InteractType.ARMOR_RACK, 9, 1),
        InteractiveObject(InteractType.ARMOR_RACK, 10, 1),
        # Side armor racks (rows 4-5)
        InteractiveObject(InteractType.ARMOR_RACK, 1, 4),
        InteractiveObject(InteractType.ARMOR_RACK, 12, 4),
        InteractiveObject(InteractType.ARMOR_RACK, 1, 5),
        InteractiveObject(InteractType.ARMOR_RACK, 12, 5),
    ],
}

# Room display names
ROOM_NAMES = {
    "main_hall": "Main Hall",
    "breakfast_hall": "Breakfast Hall",
    "armory": "Armory",
}


class Castle:
    """Manages the Dragon Castle hub: multiple rooms, doors, interactions."""

    def __init__(self):
        self.rooms = {
            "main_hall": Room.from_layout(MAIN_HALL_LAYOUT),
            "breakfast_hall": Room.from_layout(BREAKFAST_HALL_LAYOUT),
            "armory": Room.from_layout(ARMORY_LAYOUT),
        }
        self.doors = DOOR_DEFS
        self.interactives = INTERACTIVE_DEFS
        self.spawn_points = SPAWN_POINTS
        self.current_room_name = "main_hall"

        # Door transition state (ping-pong protection)
        self._on_door = False

    @property
    def current_room(self):
        return self.rooms[self.current_room_name]

    @property
    def current_room_display(self):
        return ROOM_NAMES.get(self.current_room_name, self.current_room_name)

    def get_spawn_pos(self, room_name, spawn_name):
        """Get pixel position for a named spawn point."""
        points = self.spawn_points.get(room_name, {})
        gx, gy = points.get(spawn_name, points.get("default", (3, 3)))
        return gx * TILE_SIZE, gy * TILE_SIZE

    def check_door_transition(self, player):
        """Check if player's hitbox overlaps a door. Returns (target_room, spawn_name) or None.

        Uses ping-pong protection: the player must leave the door before
        another transition can fire.
        """
        doors = self.doors.get(self.current_room_name, [])
        on_any_door = False

        for door in doors:
            if player.hitbox.colliderect(door.rect):
                on_any_door = True
                if not self._on_door:
                    self._on_door = True
                    return door.target_room, door.spawn_name

        if not on_any_door:
            self._on_door = False

        return None

    def transition_to(self, room_name, spawn_name, player):
        """Move to a new room and place the player at the spawn point."""
        self.current_room_name = room_name
        px, py = self.get_spawn_pos(room_name, spawn_name)
        player.teleport(px, py)
        self._on_door = True  # prevent immediate re-trigger

    def get_nearby_interactable(self, player):
        """Return the InteractiveObject the player is facing, or None."""
        interact_rect = player.get_interact_rect()
        interactives = self.interactives.get(self.current_room_name, [])
        for obj in interactives:
            if interact_rect.colliderect(obj.rect):
                return obj
        return None

    def update_pedestals(self, game_data):
        """Update crystal pedestal tile types based on collected crystals."""
        room = self.rooms["main_hall"]
        crystal_map = {
            "red": TileType.PEDESTAL_RED,
            "blue": TileType.PEDESTAL_BLUE,
            "green": TileType.PEDESTAL_GREEN,
        }
        for obj in self.interactives.get("main_hall", []):
            if obj.type == InteractType.CRYSTAL_PEDESTAL:
                crystal = obj.metadata.get("crystal")
                if crystal in game_data.crystals_collected:
                    room.set_tile_type(obj.grid_x, obj.grid_y,
                                       crystal_map[crystal])
