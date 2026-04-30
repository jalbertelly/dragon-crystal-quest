"""ArmorSelect — modal overlay for equipping armor."""

import pygame
from settings import (
    NATIVE_WIDTH, NATIVE_HEIGHT,
    DIALOG_BG, DIALOG_BORDER, WHITE, BLACK,
    UI_HIGHLIGHT, GRAY,
)
from items.armor import get_armor, get_armor_bonus_text


class ArmorSelect:
    """Modal armor selection overlay."""

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
        """Handle navigation. Returns True if armor was equipped, None to stay open."""
        if inp.pause:
            self.close()
            return None

        count = len(game_data.armor_inventory)
        if count == 0:
            return None

        if inp.nav_up:
            self.selected = (self.selected - 1) % count
        elif inp.nav_down:
            self.selected = (self.selected + 1) % count

        if inp.interact or inp.attack:
            armor_id = game_data.armor_inventory[self.selected]
            game_data.equip_armor(armor_id)
            self.close()
            return True

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
        title = font.render("~ Armory ~", True, UI_HIGHLIGHT)
        surface.blit(title,
                     (NATIVE_WIDTH // 2 - title.get_width() // 2, 30))

        # Current armor
        equipped = get_armor(game_data.equipped_armor)
        if equipped:
            eq_text = font_sm.render(f"Wearing: {equipped.name}", True, GRAY)
            surface.blit(eq_text,
                         (NATIVE_WIDTH // 2 - eq_text.get_width() // 2, 48))

        # Armor list
        for i, armor_id in enumerate(game_data.armor_inventory):
            armor = get_armor(armor_id)
            if armor is None:
                continue

            y = 68 + i * 38
            is_selected = i == self.selected
            is_equipped = armor_id == game_data.equipped_armor

            # Selection box
            box = pygame.Rect(24, y, NATIVE_WIDTH - 48, 34)
            if is_selected:
                pygame.draw.rect(surface, UI_HIGHLIGHT, box, 1)
            else:
                pygame.draw.rect(surface, GRAY, box, 1)

            # Armor name
            name_text = armor.name
            if is_equipped:
                name_text += " [E]"
            name_surf = font.render(name_text, True, WHITE)
            surface.blit(name_surf, (30, y + 3))

            # Bonus text
            bonus = get_armor_bonus_text(armor_id)
            bonus_surf = font_sm.render(bonus, True, GRAY)
            surface.blit(bonus_surf, (30, y + 19))

        # Controls hint
        hint = font_sm.render("[Up/Down] Select  [Enter] Equip  [Esc] Close",
                              True, GRAY)
        surface.blit(hint,
                     (NATIVE_WIDTH // 2 - hint.get_width() // 2,
                      NATIVE_HEIGHT - 16))
