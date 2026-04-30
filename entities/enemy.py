"""Enemy — base enemy class with AI state machine."""

import random
import pygame
from enum import Enum
from settings import (
    TILE_SIZE,
    ENEMY_DETECTION_RANGE, ENEMY_ATTACK_RANGE, ENEMY_ATTACK_COOLDOWN,
    ENEMY_IDLE_MIN, ENEMY_IDLE_MAX,
    ENEMY_PATROL_MIN, ENEMY_PATROL_MAX,
    ENEMY_DEFAULT_SPEED, ENEMY_DEFAULT_HP, ENEMY_DEFAULT_DAMAGE,
    ENEMY_COLOR, ENEMY_HURT_COLOR,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT,
    WHITE,
)

_next_enemy_id = 0


def _gen_id():
    global _next_enemy_id
    _next_enemy_id += 1
    return _next_enemy_id


class AIState(Enum):
    IDLE = "idle"
    PATROL = "patrol"
    CHASE = "chase"
    ATTACK = "attack"
    DEAD = "dead"


DIRECTIONS = [DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT]

DIR_VECTORS = {
    DIR_UP: (0, -1),
    DIR_DOWN: (0, 1),
    DIR_LEFT: (-1, 0),
    DIR_RIGHT: (1, 0),
}


class Enemy:
    """A basic enemy with idle/patrol/chase/attack AI."""

    SPRITE_W = 14
    SPRITE_H = 14
    HITBOX_W = 12
    HITBOX_H = 12

    def __init__(self, x, y, hp=None, damage=None, speed=None, color=None):
        self.id = _gen_id()
        self.hp = hp if hp is not None else ENEMY_DEFAULT_HP
        self.max_hp = self.hp
        self.damage = damage if damage is not None else ENEMY_DEFAULT_DAMAGE
        self.speed = speed if speed is not None else ENEMY_DEFAULT_SPEED
        self.color = color or ENEMY_COLOR
        self.direction = random.choice(DIRECTIONS)

        self.x = float(x)
        self.y = float(y)
        self.sprite_rect = pygame.Rect(int(x), int(y), self.SPRITE_W, self.SPRITE_H)
        hb_x = int(x) + (self.SPRITE_W - self.HITBOX_W) // 2
        hb_y = int(y) + (self.SPRITE_H - self.HITBOX_H) // 2
        self.hitbox = pygame.Rect(hb_x, hb_y, self.HITBOX_W, self.HITBOX_H)

        # AI
        self.state = AIState.IDLE
        self._state_timer = random.uniform(ENEMY_IDLE_MIN, ENEMY_IDLE_MAX)
        self._patrol_dir = (0, 0)
        self._attack_cooldown = 0.0
        self._stuck_frames = 0

        # Hurt flash
        self._hurt_timer = 0.0
        self._HURT_FLASH = 0.15

    # -- properties -------------------------------------------------------

    @property
    def is_dead(self):
        return self.state == AIState.DEAD

    @property
    def center(self):
        return self.hitbox.center

    # -- update -----------------------------------------------------------

    def update(self, dt, player, room, game_data):
        if self.is_dead:
            return

        # Tick hurt flash
        if self._hurt_timer > 0:
            self._hurt_timer = max(0, self._hurt_timer - dt)

        # Tick attack cooldown
        if self._attack_cooldown > 0:
            self._attack_cooldown = max(0, self._attack_cooldown - dt)

        # Distance to player
        px, py = player.hitbox.center
        ex, ey = self.hitbox.center
        dist = ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5

        # State transitions
        if self.state == AIState.IDLE:
            self._update_idle(dt, dist)
        elif self.state == AIState.PATROL:
            self._update_patrol(dt, dist, room)
        elif self.state == AIState.CHASE:
            self._update_chase(dt, dist, player, room)
        elif self.state == AIState.ATTACK:
            self._update_attack(dt, dist, player, game_data)

    def _update_idle(self, dt, dist):
        if dist <= ENEMY_DETECTION_RANGE:
            self.state = AIState.CHASE
            return
        self._state_timer -= dt
        if self._state_timer <= 0:
            self.state = AIState.PATROL
            dx, dy = DIR_VECTORS[random.choice(DIRECTIONS)]
            self._patrol_dir = (dx, dy)
            self._state_timer = random.uniform(ENEMY_PATROL_MIN, ENEMY_PATROL_MAX)
            self._stuck_frames = 0

    def _update_patrol(self, dt, dist, room):
        if dist <= ENEMY_DETECTION_RANGE:
            self.state = AIState.CHASE
            return
        self._state_timer -= dt
        if self._state_timer <= 0:
            self.state = AIState.IDLE
            self._state_timer = random.uniform(ENEMY_IDLE_MIN, ENEMY_IDLE_MAX)
            return

        dx = self._patrol_dir[0] * self.speed * dt
        dy = self._patrol_dir[1] * self.speed * dt
        moved = self._move(dx, dy, room)
        if not moved:
            self._stuck_frames += 1
            if self._stuck_frames > 10:
                # Pick a new direction
                dx, dy = DIR_VECTORS[random.choice(DIRECTIONS)]
                self._patrol_dir = (dx, dy)
                self._stuck_frames = 0

    def _update_chase(self, dt, dist, player, room):
        if dist > ENEMY_DETECTION_RANGE * 1.5:
            self.state = AIState.IDLE
            self._state_timer = random.uniform(ENEMY_IDLE_MIN, ENEMY_IDLE_MAX)
            return
        if dist <= ENEMY_ATTACK_RANGE:
            self.state = AIState.ATTACK
            return

        # Move toward player, axis-independent
        px, py = player.hitbox.center
        ex, ey = self.hitbox.center
        dx_sign = 1 if px > ex else (-1 if px < ex else 0)
        dy_sign = 1 if py > ey else (-1 if py < ey else 0)

        move_x = dx_sign * self.speed * dt
        move_y = dy_sign * self.speed * dt

        # Normalise diagonal
        if move_x and move_y:
            move_x *= 0.7071
            move_y *= 0.7071

        # Update facing direction
        if abs(px - ex) > abs(py - ey):
            self.direction = DIR_RIGHT if dx_sign > 0 else DIR_LEFT
        else:
            self.direction = DIR_DOWN if dy_sign > 0 else DIR_UP

        # Move each axis independently to slide along walls
        self._move(move_x, 0, room)
        self._move(0, move_y, room)

    def _update_attack(self, dt, dist, player, game_data):
        if dist > ENEMY_ATTACK_RANGE * 1.5:
            self.state = AIState.CHASE
            return

        if self._attack_cooldown <= 0:
            player.take_damage(self.damage, game_data)
            self._attack_cooldown = ENEMY_ATTACK_COOLDOWN

    # -- movement ---------------------------------------------------------

    def _move(self, dx, dy, room):
        """Move by (dx, dy) with wall collision. Returns True if moved."""
        old_x, old_y = self.x, self.y
        self.x += dx
        self.y += dy
        self._sync_rects()

        for wall in room.get_wall_rects():
            if not self.hitbox.colliderect(wall):
                continue
            if dx > 0:
                self.hitbox.right = wall.left
            elif dx < 0:
                self.hitbox.left = wall.right
            if dy > 0:
                self.hitbox.bottom = wall.top
            elif dy < 0:
                self.hitbox.top = wall.bottom

            self.x = float(self.hitbox.x - (self.SPRITE_W - self.HITBOX_W) // 2)
            self.y = float(self.hitbox.y - (self.SPRITE_H - self.HITBOX_H) // 2)
            self._sync_rects()

        return (self.x != old_x) or (self.y != old_y)

    def _sync_rects(self):
        self.sprite_rect.x = int(self.x)
        self.sprite_rect.y = int(self.y)
        self.hitbox.x = int(self.x) + (self.SPRITE_W - self.HITBOX_W) // 2
        self.hitbox.y = int(self.y) + (self.SPRITE_H - self.HITBOX_H) // 2

    # -- combat -----------------------------------------------------------

    def take_damage(self, amount):
        """Apply damage. Returns True if enemy died."""
        self.hp -= amount
        self._hurt_timer = self._HURT_FLASH
        if self.hp <= 0:
            self.hp = 0
            self.state = AIState.DEAD
            return True
        return False

    # -- draw -------------------------------------------------------------

    def draw(self, surface, camera):
        if self.is_dead:
            return

        draw_rect = camera.apply(self.sprite_rect)
        color = ENEMY_HURT_COLOR if self._hurt_timer > 0 else self.color
        pygame.draw.rect(surface, color, draw_rect)

        # Direction indicator
        cx, cy = draw_rect.centerx, draw_rect.centery
        s = 2
        if self.direction == DIR_UP:
            pts = [(cx, draw_rect.top - 1), (cx - s, draw_rect.top + s), (cx + s, draw_rect.top + s)]
        elif self.direction == DIR_DOWN:
            pts = [(cx, draw_rect.bottom + 1), (cx - s, draw_rect.bottom - s), (cx + s, draw_rect.bottom - s)]
        elif self.direction == DIR_LEFT:
            pts = [(draw_rect.left - 1, cy), (draw_rect.left + s, cy - s), (draw_rect.left + s, cy + s)]
        else:
            pts = [(draw_rect.right + 1, cy), (draw_rect.right - s, cy - s), (draw_rect.right - s, cy + s)]
        pygame.draw.polygon(surface, WHITE, pts)

        # HP bar above sprite
        if self.hp < self.max_hp:
            bar_w = self.SPRITE_W
            bar_h = 2
            bar_x = draw_rect.x
            bar_y = draw_rect.y - 4
            bg = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
            fill_w = int(bar_w * (self.hp / self.max_hp))
            fill = pygame.Rect(bar_x, bar_y, fill_w, bar_h)
            pygame.draw.rect(surface, (60, 0, 0), bg)
            pygame.draw.rect(surface, (0, 200, 0), fill)
