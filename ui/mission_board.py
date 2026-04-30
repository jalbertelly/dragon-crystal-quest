"""MissionBoard — modal overlay for selecting a mission."""

import pygame
from settings import (
    NATIVE_WIDTH, NATIVE_HEIGHT,
    DIALOG_BG, DIALOG_BORDER, WHITE, BLACK,
    UI_HIGHLIGHT, UI_LOCKED, GRAY,
    PEDESTAL_GLOW_RED, PEDESTAL_GLOW_BLUE, PEDESTAL_GLOW_GREEN,
)

MISSIONS = [
    {
        "id": 1,
        "name": "Dragon Volcano",
        "icon_color": PEDESTAL_GLOW_RED,
        "description": "A fiery dungeon deep within",
        "description2": "the heart of the volcano.",
    },
    {
        "id": 2,
        "name": "Frost Caves",
        "icon_color": PEDESTAL_GLOW_BLUE,
        "description": "Frozen caverns filled with",
        "description2": "icy perils and frost beasts.",
    },
    {
        "id": 3,
        "name": "Emerald Marsh",
        "icon_color": PEDESTAL_GLOW_GREEN,
        "description": "A poisonous swamp hiding",
        "description2": "ancient ruins and danger.",
    },
]


class MissionBoard:
    """Modal mission selection overlay."""

    def __init__(self):
        self.active = False
        self.selected = 0
        self._font = None
        self._font_sm = None

    def _get_fonts(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 18)
            self._font_sm = pygame.font.Font(None, 14)
        return self._font, self._font_sm

    def show(self):
        self.active = True
        self.selected = 0

    def close(self):
        self.active = False

    def handle_input(self, inp, game_data):
        """Handle navigation. Returns mission_id on confirm, None otherwise."""
        if inp.pause:
            self.close()
            return None

        if inp.nav_up:
            self.selected = (self.selected - 1) % len(MISSIONS)
        elif inp.nav_down:
            self.selected = (self.selected + 1) % len(MISSIONS)

        if inp.interact or inp.attack:
            mission = MISSIONS[self.selected]
            if game_data.is_mission_unlocked(mission["id"]):
                self.close()
                return mission["id"]

        return None

    def draw(self, surface, game_data):
        if not self.active:
            return

        font, font_sm = self._get_fonts()

        # Overlay background
        overlay = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Title
        title = font.render("~ Mission Board ~", True, UI_HIGHLIGHT)
        surface.blit(title,
                     (NATIVE_WIDTH // 2 - title.get_width() // 2, 20))

        # Mission entries
        for i, mission in enumerate(MISSIONS):
            y = 45 + i * 55
            unlocked = game_data.is_mission_unlocked(mission["id"])
            completed = mission["id"] in game_data.missions_completed
            is_selected = i == self.selected

            # Selection box
            box = pygame.Rect(20, y, NATIVE_WIDTH - 40, 48)
            if is_selected:
                pygame.draw.rect(surface, UI_HIGHLIGHT, box, 1)
            else:
                pygame.draw.rect(surface, GRAY, box, 1)

            # Mission icon
            icon_rect = pygame.Rect(26, y + 6, 12, 12)
            icon_color = mission["icon_color"] if unlocked else UI_LOCKED
            pygame.draw.rect(surface, icon_color, icon_rect)

            # Mission name
            name_color = WHITE if unlocked else UI_LOCKED
            name_surf = font.render(mission["name"], True, name_color)
            surface.blit(name_surf, (44, y + 4))

            # Status
            if completed:
                status = font_sm.render("COMPLETE", True, UI_HIGHLIGHT)
            elif unlocked:
                status = font_sm.render("AVAILABLE", True, WHITE)
            else:
                status = font_sm.render("LOCKED", True, UI_LOCKED)
            surface.blit(status, (44, y + 20))

            # Description
            if unlocked:
                desc = font_sm.render(mission["description"], True, GRAY)
                surface.blit(desc, (44, y + 32))

        # Controls hint
        hint = font_sm.render("[Up/Down] Navigate  [Enter] Select  [Esc] Close",
                              True, GRAY)
        surface.blit(hint,
                     (NATIVE_WIDTH // 2 - hint.get_width() // 2,
                      NATIVE_HEIGHT - 16))
