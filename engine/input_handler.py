"""Input handler — wraps PyGame key state with held + edge-triggered detection."""

import pygame


class InputHandler:
    def __init__(self):
        self._keys = pygame.key.get_pressed()
        self._prev_keys = self._keys

    def update(self):
        self._prev_keys = self._keys
        self._keys = pygame.key.get_pressed()

    # -- helpers ----------------------------------------------------------

    def _held(self, *scancodes):
        return any(self._keys[k] for k in scancodes)

    def _just_pressed(self, *scancodes):
        return any(self._keys[k] and not self._prev_keys[k] for k in scancodes)

    # -- continuous (held) inputs -----------------------------------------

    @property
    def move_up(self):
        return self._held(pygame.K_UP, pygame.K_w)

    @property
    def move_down(self):
        return self._held(pygame.K_DOWN, pygame.K_s)

    @property
    def move_left(self):
        return self._held(pygame.K_LEFT, pygame.K_a)

    @property
    def move_right(self):
        return self._held(pygame.K_RIGHT, pygame.K_d)

    # -- one-shot navigation (for menus) -----------------------------------

    @property
    def nav_up(self):
        return self._just_pressed(pygame.K_UP, pygame.K_w)

    @property
    def nav_down(self):
        return self._just_pressed(pygame.K_DOWN, pygame.K_s)

    # -- one-shot (edge-triggered) inputs ---------------------------------

    @property
    def attack(self):
        return self._just_pressed(pygame.K_z, pygame.K_SPACE)

    @property
    def special(self):
        return self._just_pressed(pygame.K_x, pygame.K_LSHIFT)

    @property
    def interact(self):
        return self._just_pressed(pygame.K_RETURN)

    @property
    def pause(self):
        return self._just_pressed(pygame.K_ESCAPE)
