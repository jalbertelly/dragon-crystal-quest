"""Camera — follows a target entity, clamped to room bounds."""

from settings import TILE_SIZE


class Camera:
    def __init__(self, view_w, view_h):
        self.x = 0
        self.y = 0
        self.view_w = view_w
        self.view_h = view_h

    def update(self, target, room):
        """Center on *target* (must expose a `hitbox` rect), clamped to *room*."""
        self.x = target.hitbox.centerx - self.view_w // 2
        self.y = target.hitbox.centery - self.view_h // 2

        room_px_w = room.width * TILE_SIZE
        room_px_h = room.height * TILE_SIZE

        max_x = max(0, room_px_w - self.view_w)
        max_y = max(0, room_px_h - self.view_h)

        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def apply(self, rect):
        """Return a copy of *rect* shifted by the camera offset (int-aligned)."""
        return rect.move(-int(self.x), -int(self.y))
