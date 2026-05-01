"""Hazard — environmental hazard damage tracker for dungeon rooms."""

from settings import (
    TILE_SIZE,
    HAZARD_DAMAGE,
    HAZARD_LAVA_INTERVAL,
    HAZARD_POISON_INTERVAL,
    HAZARD_ICE_SPEED_MULT,
)
from world.tile import TileType
from combat.damage import DamageType, apply_armor_resist


# Map hazard tile types to their damage type and tick interval
_HAZARD_CONFIG = {
    TileType.HAZARD_LAVA: (DamageType.FIRE, HAZARD_LAVA_INTERVAL),
    TileType.HAZARD_POISON: (DamageType.POISON, HAZARD_POISON_INTERVAL),
}


class HazardTracker:
    """Checks player position against hazard tiles and applies damage."""

    def __init__(self):
        self._tick_timer = 0.0
        self._on_hazard = False

    def update(self, dt, player, room, game_data):
        """Check hazard tiles under the player and apply effects.

        Returns True if the player is currently on an ice tile (for speed
        adjustment by the caller).
        """
        # Check tile at the bottom-center of the player hitbox (feet)
        foot_x = int(player.hitbox.centerx) // TILE_SIZE
        foot_y = int(player.hitbox.bottom - 1) // TILE_SIZE
        tile = room.get_tile(foot_x, foot_y)

        on_ice = False

        if tile is None or tile.type not in _HAZARD_CONFIG and tile.type != TileType.HAZARD_ICE:
            # Not on a hazard — reset timer
            self._tick_timer = 0.0
            self._on_hazard = False
            return False

        if tile.type == TileType.HAZARD_ICE:
            on_ice = True
            # Ice doesn't deal damage
            self._tick_timer = 0.0
            self._on_hazard = False
            return True

        # Damage hazard (lava or poison)
        damage_type, interval = _HAZARD_CONFIG[tile.type]
        self._on_hazard = True

        self._tick_timer += dt
        if self._tick_timer >= interval:
            self._tick_timer -= interval
            # Only deal damage if player is not invincible
            if not player.is_invincible:
                effective = apply_armor_resist(
                    HAZARD_DAMAGE, game_data.equipped_armor, damage_type
                )
                player.take_damage(effective, game_data)

        return on_ice
