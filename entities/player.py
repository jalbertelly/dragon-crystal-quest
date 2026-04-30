"""Player entity — movement, collision, interaction, and placeholder rendering."""

import pygame
from settings import (
    PLAYER_SPEED, PLAYER_SPRITE_WIDTH, PLAYER_SPRITE_HEIGHT,
    PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT, PLAYER_INTERACT_RANGE,
    RED, WHITE, TEAL,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT,
    TILE_SIZE,
)


class Player:
    def __init__(self, x, y, character="russell"):
        self.character = character
        self.color = RED if character == "russell" else TEAL
        self.speed = PLAYER_SPEED
        self.direction = DIR_DOWN

        # Float position (top-left of *sprite*)
        self.x = float(x)
        self.y = float(y)

        # Visual sprite rect
        self.sprite_rect = pygame.Rect(x, y,
                                       PLAYER_SPRITE_WIDTH,
                                       PLAYER_SPRITE_HEIGHT)

        # Collision hitbox — smaller rect anchored at feet
        hb_x = x + (PLAYER_SPRITE_WIDTH - PLAYER_HITBOX_WIDTH) // 2
        hb_y = y + PLAYER_SPRITE_HEIGHT - PLAYER_HITBOX_HEIGHT
        self.hitbox = pygame.Rect(hb_x, hb_y,
                                  PLAYER_HITBOX_WIDTH,
                                  PLAYER_HITBOX_HEIGHT)

    # -- update -----------------------------------------------------------

    def update(self, dt, inp, room):
        dx, dy = 0.0, 0.0

        if inp.move_up:
            dy -= self.speed * dt
            self.direction = DIR_UP
        if inp.move_down:
            dy += self.speed * dt
            self.direction = DIR_DOWN
        if inp.move_left:
            dx -= self.speed * dt
            self.direction = DIR_LEFT
        if inp.move_right:
            dx += self.speed * dt
            self.direction = DIR_RIGHT

        # Normalise diagonal movement so it isn't faster
        if dx and dy:
            factor = 0.7071  # 1/sqrt(2)
            dx *= factor
            dy *= factor

        # Move on each axis independently for clean collision
        self._move_axis(dx, 0, room)
        self._move_axis(0, dy, room)

    def _move_axis(self, dx, dy, room):
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

            self.x = float(self.hitbox.x
                           - (PLAYER_SPRITE_WIDTH - PLAYER_HITBOX_WIDTH) // 2)
            self.y = float(self.hitbox.y
                           - (PLAYER_SPRITE_HEIGHT - PLAYER_HITBOX_HEIGHT))
            self._sync_rects()

    def _sync_rects(self):
        self.sprite_rect.x = int(self.x)
        self.sprite_rect.y = int(self.y)

        self.hitbox.x = int(self.x) + (PLAYER_SPRITE_WIDTH
                                        - PLAYER_HITBOX_WIDTH) // 2
        self.hitbox.y = (int(self.y) + PLAYER_SPRITE_HEIGHT
                         - PLAYER_HITBOX_HEIGHT)

    # -- interaction ------------------------------------------------------

    def get_interact_rect(self):
        """Return a small rect in front of the player for interaction checks."""
        r = PLAYER_INTERACT_RANGE
        hb = self.hitbox
        if self.direction == DIR_UP:
            return pygame.Rect(hb.x, hb.y - r, hb.width, r)
        elif self.direction == DIR_DOWN:
            return pygame.Rect(hb.x, hb.bottom, hb.width, r)
        elif self.direction == DIR_LEFT:
            return pygame.Rect(hb.x - r, hb.y, r, hb.height)
        else:  # DIR_RIGHT
            return pygame.Rect(hb.right, hb.y, r, hb.height)

    def teleport(self, x, y):
        """Instantly move the player to a position (in pixels)."""
        self.x = float(x)
        self.y = float(y)
        self._sync_rects()

    # -- draw -------------------------------------------------------------

    def draw(self, surface, camera):
        draw_rect = camera.apply(self.sprite_rect)
        pygame.draw.rect(surface, self.color, draw_rect)

        # Direction indicator (small triangle)
        cx, cy = draw_rect.centerx, draw_rect.centery
        s = 3
        if self.direction == DIR_UP:
            pts = [(cx, draw_rect.top - 2),
                   (cx - s, draw_rect.top + s),
                   (cx + s, draw_rect.top + s)]
        elif self.direction == DIR_DOWN:
            pts = [(cx, draw_rect.bottom + 2),
                   (cx - s, draw_rect.bottom - s),
                   (cx + s, draw_rect.bottom - s)]
        elif self.direction == DIR_LEFT:
            pts = [(draw_rect.left - 2, cy),
                   (draw_rect.left + s, cy - s),
                   (draw_rect.left + s, cy + s)]
        else:
            pts = [(draw_rect.right + 2, cy),
                   (draw_rect.right - s, cy - s),
                   (draw_rect.right - s, cy + s)]
        pygame.draw.polygon(surface, WHITE, pts)

        # Debug: draw hitbox outline
        hb_draw = camera.apply(self.hitbox)
        pygame.draw.rect(surface, (255, 255, 0), hb_draw, 1)
