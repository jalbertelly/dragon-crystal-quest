"""HUD — in-game heads-up display (heart bar, room name)."""

import pygame
from settings import (
    HEART_FULL, HEART_EMPTY, WHITE, BLACK,
    NATIVE_WIDTH,
)


class HUD:
    """Draws the heart bar and optional room label."""

    HEART_SIZE = 8
    HEART_SPACING = 2
    MARGIN = 4

    def __init__(self):
        self._font = None
        self.room_label = ""

    def _get_font(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 14)
        return self._font

    def draw(self, surface, game_data):
        self._draw_hearts(surface, game_data.hp, game_data.max_hp)
        if self.room_label:
            self._draw_room_label(surface)

    def _draw_hearts(self, surface, hp, max_hp):
        m = self.MARGIN
        s = self.HEART_SIZE
        sp = self.HEART_SPACING

        for i in range(max_hp):
            x = m + i * (s + sp)
            y = m
            rect = pygame.Rect(x, y, s, s)

            color = HEART_FULL if i < hp else HEART_EMPTY
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

    def _draw_room_label(self, surface):
        font = self._get_font()
        text_surf = font.render(self.room_label, True, WHITE)
        x = NATIVE_WIDTH - text_surf.get_width() - self.MARGIN
        surface.blit(text_surf, (x, self.MARGIN))
