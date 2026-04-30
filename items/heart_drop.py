"""HeartDrop — collectible health pickup spawned by enemy deaths."""

import random
import pygame
from settings import (
    HEART_SMALL_HEAL, HEART_LARGE_HEAL,
    HEART_DROP_CHANCE_LARGE, HEART_DROP_CHANCE_SMALL,
    HEART_DROP_LIFETIME,
    HEART_SMALL_COLOR, HEART_LARGE_COLOR, WHITE,
)


class HeartDrop:
    """A health pickup on the ground."""

    SIZE = 8

    def __init__(self, x, y, heal_amount, color):
        self.x = x
        self.y = y
        self.heal_amount = heal_amount
        self.color = color
        self.rect = pygame.Rect(int(x) - self.SIZE // 2,
                                int(y) - self.SIZE // 2,
                                self.SIZE, self.SIZE)
        self.lifetime = HEART_DROP_LIFETIME
        self.alive = True

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def try_pickup(self, player_hitbox, game_data):
        """Check if player is touching this drop. Returns True if picked up."""
        if not self.alive:
            return False
        if player_hitbox.colliderect(self.rect):
            game_data.heal(self.heal_amount)
            self.alive = False
            return True
        return False

    def draw(self, surface, camera):
        if not self.alive:
            return
        # Blink when about to expire (last 3 seconds)
        if self.lifetime < 3.0 and int(self.lifetime * 4) % 2 == 0:
            return
        draw_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, self.color, draw_rect)
        # Cross/plus shape for heart visual
        cx, cy = draw_rect.centerx, draw_rect.centery
        pygame.draw.line(surface, WHITE, (cx - 2, cy), (cx + 2, cy))
        pygame.draw.line(surface, WHITE, (cx, cy - 2), (cx, cy + 2))


def roll_heart_drop(x, y):
    """Roll the loot table and return a HeartDrop or None.

    Exclusive rolls: large (5%) > small (30%) > nothing.
    """
    roll = random.random()
    if roll < HEART_DROP_CHANCE_LARGE:
        return HeartDrop(x, y, HEART_LARGE_HEAL, HEART_LARGE_COLOR)
    elif roll < HEART_DROP_CHANCE_LARGE + HEART_DROP_CHANCE_SMALL:
        return HeartDrop(x, y, HEART_SMALL_HEAL, HEART_SMALL_COLOR)
    return None
