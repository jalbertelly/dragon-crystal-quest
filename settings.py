"""Global constants for Dragon Crystal Quest."""

# Window
TITLE = "Dragon Crystal Quest"
FPS = 60
MAX_DT = 0.05  # clamp delta-time to prevent tunnelling on hitches

# Native resolution (NES-style), scaled up for display
NATIVE_WIDTH = 256
NATIVE_HEIGHT = 240
SCALE = 3
WINDOW_WIDTH = NATIVE_WIDTH * SCALE
WINDOW_HEIGHT = NATIVE_HEIGHT * SCALE

# Tiles
TILE_SIZE = 16

# Player
PLAYER_SPEED = 80  # pixels per second
PLAYER_SPRITE_WIDTH = 16
PLAYER_SPRITE_HEIGHT = 24
PLAYER_HITBOX_WIDTH = 12  # smaller hitbox at feet
PLAYER_HITBOX_HEIGHT = 10
PLAYER_MAX_HP = 10
PLAYER_INTERACT_RANGE = 4  # pixels beyond hitbox edge for interact probe

# Colors (placeholders)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
TEAL = (50, 200, 180)
DARK_GRAY = (60, 60, 60)
GRAY = (120, 120, 120)
BROWN = (139, 90, 43)
DARK_GREEN = (20, 80, 20)
FLOOR_COLOR = (100, 90, 80)
FLOOR_COLOR_ALT = (92, 83, 74)
WALL_COLOR = (50, 45, 40)
WALL_HIGHLIGHT = (70, 63, 56)

# Castle-specific colors
CARPET_COLOR = (120, 30, 30)
CARPET_COLOR_ALT = (110, 25, 25)
DOOR_COLOR = (100, 70, 30)
DOOR_FRAME_COLOR = (130, 90, 40)
PEDESTAL_COLOR = (140, 140, 150)
PEDESTAL_GLOW_RED = (255, 80, 80)
PEDESTAL_GLOW_BLUE = (80, 150, 255)
PEDESTAL_GLOW_GREEN = (80, 255, 120)
TABLE_COLOR = (110, 70, 35)
FOOD_COLOR = (200, 160, 60)
ARMOR_RACK_COLOR = (90, 80, 70)
BOARD_COLOR = (160, 130, 80)
BANNER_COLOR = (150, 40, 40)
TORCH_COLOR = (255, 180, 50)

# UI Colors
HEART_FULL = (220, 30, 30)
HEART_EMPTY = (80, 40, 40)
DIALOG_BG = (20, 20, 40)
DIALOG_BORDER = (180, 160, 100)
UI_HIGHLIGHT = (255, 220, 80)
UI_LOCKED = (100, 100, 100)

# Directions
DIR_UP = "up"
DIR_DOWN = "down"
DIR_LEFT = "left"
DIR_RIGHT = "right"

# Game states (scene-level)
STATE_TITLE = "title"
STATE_CASTLE = "castle"
STATE_PLAYING = "playing"
STATE_PAUSE = "pause"

# Modal UI substates (overlay on top of scene)
MODAL_NONE = "none"
MODAL_DIALOG = "dialog"
MODAL_MISSION_BOARD = "mission_board"
MODAL_ARMOR_SELECT = "armor_select"

# Door transition cooldown (seconds)
DOOR_COOLDOWN = 0.3

# Combat — Melee
MELEE_COOLDOWN = 0.3       # seconds between swings
MELEE_DURATION = 0.15      # seconds the hitbox stays active
MELEE_RANGE = TILE_SIZE    # 1 tile in front of player
MELEE_DAMAGE = 1

# Combat — Invincibility frames
INVINCIBILITY_DURATION = 1.0   # seconds of i-frames after taking damage
FLASH_INTERVAL = 0.1           # seconds per visibility toggle during i-frames

# Combat — Enemies
ENEMY_DETECTION_RANGE = 80     # pixels — switch to chase
ENEMY_ATTACK_RANGE = 18        # pixels — close enough to melee
ENEMY_ATTACK_COOLDOWN = 1.0    # seconds between enemy attacks
ENEMY_IDLE_MIN = 0.5
ENEMY_IDLE_MAX = 2.0
ENEMY_PATROL_MIN = 1.0
ENEMY_PATROL_MAX = 3.0
ENEMY_DEFAULT_SPEED = 40       # pixels per second
ENEMY_DEFAULT_HP = 3
ENEMY_DEFAULT_DAMAGE = 1

# Combat — Health drops
HEART_SMALL_HEAL = 1
HEART_LARGE_HEAL = 3
HEART_DROP_CHANCE_LARGE = 0.05   # 5% chance for large heart
HEART_DROP_CHANCE_SMALL = 0.30   # 30% chance for small heart (else nothing)
HEART_DROP_LIFETIME = 10.0       # seconds before despawn

# Combat — Colors
ENEMY_COLOR = (180, 50, 180)
ENEMY_HURT_COLOR = (255, 255, 255)
MELEE_COLOR = (255, 255, 100)
HEART_SMALL_COLOR = (255, 100, 100)
HEART_LARGE_COLOR = (255, 50, 50)
