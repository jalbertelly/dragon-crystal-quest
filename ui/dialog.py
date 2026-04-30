"""DialogBox — text overlay at the bottom of the screen."""

import pygame
from settings import (
    NATIVE_WIDTH, NATIVE_HEIGHT, TILE_SIZE,
    DIALOG_BG, DIALOG_BORDER, WHITE, BLACK,
)


class DialogBox:
    """A simple text dialog displayed at the bottom of the native surface."""

    PADDING = 4
    BOX_HEIGHT = 40
    LINE_HEIGHT = 10

    def __init__(self):
        self.active = False
        self.lines = []
        self._page = 0
        self._lines_per_page = 3
        self._font = None

    def _get_font(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 16)
        return self._font

    def show(self, text):
        """Show a dialog with the given text. Text can contain newlines."""
        self.active = True
        self.lines = text.strip().split("\n")
        self._page = 0

    def advance(self):
        """Advance to next page or close if at end."""
        self._page += 1
        start = self._page * self._lines_per_page
        if start >= len(self.lines):
            self.close()

    def close(self):
        self.active = False
        self.lines = []
        self._page = 0

    def draw(self, surface):
        if not self.active:
            return

        font = self._get_font()
        p = self.PADDING
        box_y = NATIVE_HEIGHT - self.BOX_HEIGHT - p
        box_rect = pygame.Rect(p, box_y,
                               NATIVE_WIDTH - 2 * p, self.BOX_HEIGHT)

        # Background
        pygame.draw.rect(surface, DIALOG_BG, box_rect)
        pygame.draw.rect(surface, DIALOG_BORDER, box_rect, 1)

        # Text
        start = self._page * self._lines_per_page
        end = start + self._lines_per_page
        visible_lines = self.lines[start:end]

        for i, line in enumerate(visible_lines):
            text_surf = font.render(line, True, WHITE)
            surface.blit(text_surf,
                         (box_rect.x + p + 2,
                          box_rect.y + p + i * self.LINE_HEIGHT))

        # "More" indicator
        if end < len(self.lines):
            indicator = font.render("v", True, DIALOG_BORDER)
            surface.blit(indicator,
                         (box_rect.right - 10, box_rect.bottom - 10))
