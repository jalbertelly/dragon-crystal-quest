"""Game — top-level class owning the main loop and game state."""

import sys
import pygame
from settings import (
    TITLE, FPS, MAX_DT,
    NATIVE_WIDTH, NATIVE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, STATE_CASTLE, STATE_PLAYING,
    MODAL_NONE, MODAL_DIALOG, MODAL_MISSION_BOARD, MODAL_ARMOR_SELECT,
    MELEE_DAMAGE, TILE_SIZE,
)
from engine.input_handler import InputHandler
from engine.camera import Camera
from engine.game_data import GameData
from entities.player import Player
from entities.enemy import Enemy
from world.castle import Castle
from world.room import Room
from world.interactive import InteractType
from combat.melee import MeleeAttack
from items.heart_drop import roll_heart_drop
from ui.hud import HUD
from ui.dialog import DialogBox
from ui.mission_board import MissionBoard
from ui.armor_select import ArmorSelect


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.native_surface = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_CASTLE

        self.input = InputHandler()
        self.game_data = GameData()

        # Castle hub
        self.castle = Castle()
        spawn_x, spawn_y = self.castle.get_spawn_pos("main_hall", "default")
        self.player = Player(spawn_x, spawn_y,
                             character=self.game_data.selected_character)
        self.camera = Camera(NATIVE_WIDTH, NATIVE_HEIGHT)

        # UI layers
        self.hud = HUD()
        self.dialog = DialogBox()
        self.mission_board = MissionBoard()
        self.armor_select = ArmorSelect()
        self.modal = MODAL_NONE

        # Combat
        self.melee = MeleeAttack()
        self.enemies = []
        self.heart_drops = []
        self.dungeon_room = None  # set when entering a mission

        # Show opening scene on first visit to breakfast hall
        self._trigger_opening_scene()

    # -- main loop --------------------------------------------------------

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, MAX_DT)
            self._handle_events()
            self._update(dt)
            self._draw()

    # -- per-frame steps --------------------------------------------------

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.input.update()

    def _update(self, dt):
        if self.state == STATE_CASTLE:
            self._update_castle(dt)
        elif self.state == STATE_PLAYING:
            self._update_playing(dt)

    def _update_castle(self, dt):
        # Modal UI captures all input
        if self.modal != MODAL_NONE:
            self._update_modal()
            return

        # Pause
        if self.input.pause:
            self.running = False  # placeholder — will become pause menu

        # Player movement
        self.player.update(dt, self.input, self.castle.current_room)

        # Door transitions
        result = self.castle.check_door_transition(self.player)
        if result:
            target_room, spawn_name = result
            self.castle.transition_to(target_room, spawn_name, self.player)
            self.hud.room_label = self.castle.current_room_display
            # Force camera update for new room
            self.camera.update(self.player, self.castle.current_room)

            # Check for opening scene trigger
            if (target_room == "breakfast_hall"
                    and not self.game_data.opening_scene_done):
                self._show_opening_scene()
            return

        # Interact
        if self.input.interact:
            interactable = self.castle.get_nearby_interactable(self.player)
            if interactable:
                self._handle_interaction(interactable)

        # Camera
        self.camera.update(self.player, self.castle.current_room)

    def _update_modal(self):
        if self.modal == MODAL_DIALOG:
            if self.input.interact or self.input.attack:
                self.dialog.advance()
                if not self.dialog.active:
                    self.modal = MODAL_NONE

        elif self.modal == MODAL_MISSION_BOARD:
            result = self.mission_board.handle_input(self.input, self.game_data)
            if not self.mission_board.active:
                self.modal = MODAL_NONE
            if result is not None:
                self._start_mission(result)

        elif self.modal == MODAL_ARMOR_SELECT:
            result = self.armor_select.handle_input(self.input, self.game_data)
            if not self.armor_select.active:
                self.modal = MODAL_NONE
            if result:
                self.dialog.show(
                    f"Equipped: {self.game_data.equipped_armor.replace('_', ' ').title()}"
                )
                self.modal = MODAL_DIALOG

    # -- interactions -----------------------------------------------------

    def _handle_interaction(self, obj):
        if obj.type == InteractType.MISSION_BOARD:
            self.mission_board.show()
            self.modal = MODAL_MISSION_BOARD

        elif obj.type == InteractType.ARMOR_RACK:
            self.armor_select.show()
            self.modal = MODAL_ARMOR_SELECT

        elif obj.type == InteractType.BREAKFAST_TABLE:
            self.game_data.restore_hp()
            self.dialog.show(
                "You enjoy a hearty breakfast!\n"
                "HP fully restored!"
            )
            self.modal = MODAL_DIALOG

        elif obj.type == InteractType.CRYSTAL_PEDESTAL:
            crystal = obj.metadata.get("crystal", "")
            if crystal in self.game_data.crystals_collected:
                names = {"red": "Red", "blue": "Blue", "green": "Green"}
                self.dialog.show(
                    f"The {names.get(crystal, crystal)} Crystal\n"
                    "glows with power..."
                )
            else:
                self.dialog.show("An empty pedestal awaits\na crystal...")
            self.modal = MODAL_DIALOG

    def _start_mission(self, mission_id):
        """Enter a test dungeon room with enemies for combat testing."""
        self.state = STATE_PLAYING
        self.dungeon_room = self._create_test_dungeon()
        self.player.teleport(5 * TILE_SIZE, 5 * TILE_SIZE)
        self.enemies = self._spawn_test_enemies()
        self.heart_drops = []
        self.melee = MeleeAttack()
        self.hud.room_label = "Test Dungeon"
        self.camera.update(self.player, self.dungeon_room)

    def _create_test_dungeon(self):
        """Build a simple arena room for combat testing."""
        layout = (
            "####################\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "#..................#\n"
            "####################"
        )
        return Room.from_layout(layout)

    def _spawn_test_enemies(self):
        """Spawn a handful of enemies in the test dungeon."""
        positions = [
            (12 * TILE_SIZE, 4 * TILE_SIZE),
            (15 * TILE_SIZE, 8 * TILE_SIZE),
            (8 * TILE_SIZE, 11 * TILE_SIZE),
            (14 * TILE_SIZE, 12 * TILE_SIZE),
        ]
        return [Enemy(x, y) for x, y in positions]

    # -- playing state (dungeon combat) -----------------------------------

    def _update_playing(self, dt):
        """Update loop for the dungeon/combat state."""
        if self.modal != MODAL_NONE:
            self._update_modal()
            return

        if self.input.pause:
            # Return to castle on pause (placeholder)
            self.state = STATE_CASTLE
            self.castle.current_room_name = "main_hall"
            spawn_x, spawn_y = self.castle.get_spawn_pos("main_hall", "default")
            self.player.teleport(spawn_x, spawn_y)
            self.hud.room_label = self.castle.current_room_display
            self.game_data.restore_hp()
            return

        room = self.dungeon_room

        # Player movement
        self.player.update(dt, self.input, room)

        # Melee attack
        self.melee.update(dt)
        if self.input.attack:
            self.melee.try_attack(self.player)

        # Check melee hits on enemies
        atk_hb = self.melee.get_hitbox()
        if atk_hb:
            for enemy in self.enemies:
                if enemy.is_dead:
                    continue
                if self.melee.already_hit(enemy.id):
                    continue
                if atk_hb.colliderect(enemy.hitbox):
                    self.melee.register_hit(enemy.id)
                    died = enemy.take_damage(MELEE_DAMAGE)
                    if died:
                        drop = roll_heart_drop(*enemy.center)
                        if drop:
                            self.heart_drops.append(drop)

        # Update enemies (authoritative damage to player)
        for enemy in self.enemies:
            enemy.update(dt, self.player, room, self.game_data)

        # Remove dead enemies
        self.enemies = [e for e in self.enemies if not e.is_dead]

        # Update heart drops
        for drop in self.heart_drops:
            drop.update(dt)
            drop.try_pickup(self.player.hitbox, self.game_data)
        self.heart_drops = [d for d in self.heart_drops if d.alive]

        # Check player death
        if self.game_data.hp <= 0:
            self.dialog.show(
                "You have been defeated!\n"
                "Returning to Dragon Castle..."
            )
            self.modal = MODAL_DIALOG
            self.state = STATE_CASTLE
            self.castle.current_room_name = "main_hall"
            spawn_x, spawn_y = self.castle.get_spawn_pos("main_hall", "default")
            self.player.teleport(spawn_x, spawn_y)
            self.hud.room_label = self.castle.current_room_display
            self.game_data.restore_hp()
            return

        # Camera
        self.camera.update(self.player, room)

    # -- opening scene ----------------------------------------------------

    def _trigger_opening_scene(self):
        """Set up the opening scene on game start."""
        # Start in the main hall with intro text
        self.hud.room_label = self.castle.current_room_display
        self.dialog.show(
            "Welcome to Dragon Castle!\n"
            "Visit the Breakfast Hall to eat,\n"
            "the Armory for gear, or the\n"
            "Mission Board to start a quest."
        )
        self.modal = MODAL_DIALOG

    def _show_opening_scene(self):
        """Show the Breakfast Hall opening cutscene (first visit)."""
        self.game_data.opening_scene_done = True
        self.game_data.restore_hp()
        self.dialog.show(
            "The smell of roasted meat fills\n"
            "the hall. Your dragon sits down\n"
            "for a hearty breakfast before\n"
            "the adventure begins.\n"
            "HP fully restored!"
        )
        self.modal = MODAL_DIALOG

    # -- drawing ----------------------------------------------------------

    def _draw(self):
        self.native_surface.fill(BLACK)

        if self.state == STATE_CASTLE:
            self.castle.current_room.draw(self.native_surface, self.camera)
            self.player.draw(self.native_surface, self.camera)

        elif self.state == STATE_PLAYING and self.dungeon_room:
            self.dungeon_room.draw(self.native_surface, self.camera)

            # Draw heart drops (under entities)
            for drop in self.heart_drops:
                drop.draw(self.native_surface, self.camera)

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.native_surface, self.camera)

            # Draw player
            self.player.draw(self.native_surface, self.camera)

            # Draw melee attack hitbox
            self.melee.draw(self.native_surface, self.camera)

        # HUD (always on top of game world)
        self.hud.draw(self.native_surface, self.game_data)

        # Modal overlays
        if self.modal == MODAL_DIALOG:
            self.dialog.draw(self.native_surface)
        elif self.modal == MODAL_MISSION_BOARD:
            self.mission_board.draw(self.native_surface, self.game_data)
        elif self.modal == MODAL_ARMOR_SELECT:
            self.armor_select.draw(self.native_surface, self.game_data)

        # Scale pixel-art surface to window
        scaled = pygame.transform.scale(self.native_surface,
                                        (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()
