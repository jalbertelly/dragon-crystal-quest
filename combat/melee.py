"""MeleeAttack — player claw-swipe hitbox with cooldown and single-hit-per-swing."""

import pygame
from settings import (
    MELEE_COOLDOWN, MELEE_DURATION, MELEE_RANGE, MELEE_DAMAGE,
    PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT,
)


class MeleeAttack:
    """Manages the player's melee attack state, cooldown, and hitbox."""

    def __init__(self):
        self.cooldown_timer = 0.0
        self.active_timer = 0.0
        self._direction = DIR_DOWN
        self._origin_rect = pygame.Rect(0, 0, 0, 0)
        self._already_hit = set()  # enemy ids hit this swing

    @property
    def is_active(self):
        return self.active_timer > 0

    @property
    def on_cooldown(self):
        return self.cooldown_timer > 0

    def try_attack(self, player):
        """Start a melee swing if off cooldown. Returns True if attack started."""
        if self.on_cooldown or self.is_active:
            return False
        self.active_timer = MELEE_DURATION
        self.cooldown_timer = MELEE_COOLDOWN
        self._direction = player.direction
        self._origin_rect = player.hitbox.copy()
        self._already_hit.clear()
        return True

    def update(self, dt):
        if self.active_timer > 0:
            self.active_timer = max(0, self.active_timer - dt)
        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0, self.cooldown_timer - dt)

    def get_hitbox(self):
        """Return the attack hitbox Rect, or None if not active."""
        if not self.is_active:
            return None
        return _directional_rect(self._origin_rect, self._direction,
                                 MELEE_RANGE)

    def register_hit(self, enemy_id):
        """Mark an enemy as hit this swing to prevent multi-hit."""
        self._already_hit.add(enemy_id)

    def already_hit(self, enemy_id):
        return enemy_id in self._already_hit

    def draw(self, surface, camera):
        """Draw the melee hitbox as a visual indicator."""
        hb = self.get_hitbox()
        if hb is None:
            return
        from settings import MELEE_COLOR
        draw_rect = camera.apply(hb)
        s = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        s.fill((*MELEE_COLOR, 120))
        surface.blit(s, draw_rect.topleft)


def _directional_rect(hitbox, direction, reach):
    """Create a rect extending *reach* pixels in *direction* from *hitbox*."""
    if direction == DIR_UP:
        return pygame.Rect(hitbox.x, hitbox.y - reach, hitbox.width, reach)
    elif direction == DIR_DOWN:
        return pygame.Rect(hitbox.x, hitbox.bottom, hitbox.width, reach)
    elif direction == DIR_LEFT:
        return pygame.Rect(hitbox.x - reach, hitbox.y, reach, hitbox.height)
    else:  # DIR_RIGHT
        return pygame.Rect(hitbox.right, hitbox.y, reach, hitbox.height)
