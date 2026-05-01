# 🐉 Dragon Crystal Quest — Game Design & Implementation Plan

## 1. Game Overview

**Title:** Dragon Crystal Quest
**Genre:** 2D Top-Down Action RPG (8-bit pixel art style)
**Inspirations:** The Legend of Zelda (NES), Final Fantasy (NES)
**Engine:** Python 3.x + PyGame
**Art Pipeline:** PixelLab.ai for pixel-based asset generation

The player controls one of two dragons — **Russell** (Red) or **Max** (Teal) — on a quest to retrieve three magical crystals from dangerous dungeons. Each crystal unlocks a new special power. Between missions, the player returns to **Dragon Castle** to swap armor and embark on the next adventure.

---

## 2. Core Design Decisions

| Decision | Choice |
|---|---|
| Character selection | Purely cosmetic (same stats/gameplay) |
| Camera / view | Top-down (classic Zelda-style) |
| Combat | Real-time action |
| Dungeon generation | Procedurally generated rooms |
| Player stats | Simple HP bar (no leveling system) |
| Health recovery | Enemy drops (hearts/food) |
| Armor acquisition | Found as loot in dungeons |
| Save system | Save/load progress between sessions |

---

## 3. Characters

### Playable Characters
| Name | Color | Description |
|---|---|---|
| **Russell** | Red Dragon | A bold, fiery dragon with crimson scales |
| **Max** | Teal Dragon | A cool, clever dragon with teal scales |

Both characters share the same hitbox, stats, and moveset. The difference is purely sprite/palette based.

### Sprite Requirements (per character)
- Idle animation (4 directions × 2 frames)
- Walk animation (4 directions × 4 frames)
- Melee attack animation (4 directions × 3 frames)
- Special attack animation (4 directions × 3 frames)
- Hurt animation (1 direction × 2 frames)
- Death animation (4 frames)

---

## 4. Controls

| Input | Action |
|---|---|
| Arrow Keys / WASD | Move (4-directional) |
| Z / Space | Melee Attack (claw swipe) |
| X / Left Shift | Special Attack (unlocked via crystals) |
| Enter | Interact / Confirm |
| Escape | Pause Menu |
| 1, 2, 3 | Cycle special attack (once multiple are unlocked) |

---

## 5. Game Flow

```
┌─────────────────────────────────────────────────┐
│                  TITLE SCREEN                    │
│         New Game  /  Continue  /  Quit           │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              CHARACTER SELECT                    │
│          Russell (Red)  /  Max (Teal)            │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              DRAGON CASTLE (Hub)                 │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Breakfast │  │  Armory  │  │ Mission Board │  │
│  │   Hall    │  │          │  │               │  │
│  └──────────┘  └──────────┘  └───────┬───────┘  │
└──────────────────────────────────────┼──────────┘
                                       │
                       ┌───────────────┼───────────────┐
                       ▼               ▼               ▼
              ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
              │   Mission 1  │ │   Mission 2  │ │   Mission 3  │
              │Dragon Volcano│ │  Frost Caves │ │ Emerald Marsh│
              │ (Red Crystal)│ │(Blue Crystal)│ │(Green Crystal│
              └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                     │                │                │
                     ▼                ▼                ▼
              Return to Castle with Crystal → Unlock Power
```

---

## 6. Locations

### 6.1 Dragon Castle (Hub World)

A fixed, handcrafted map serving as the home base. Contains:

- **Breakfast Hall:** Opening cutscene location. The player's dragon eats breakfast here to begin the adventure. Restores HP to full when visited.
- **Armory:** Displays all collected armor sets on racks. Player walks up to an armor stand and presses Interact to equip. Shows stat comparison.
- **Mission Board:** A large map on the wall showing available missions. Player walks up and selects the next mission to embark.
- **Crystal Pedestals:** Three empty pedestals that light up as crystals are collected, providing visual progress tracking.

### 6.2 Mission 1 — Dragon Volcano 🌋

- **Theme:** Lava, magma rivers, volcanic rock, fire geysers
- **Color Palette:** Red, orange, dark brown, black
- **Environmental Hazards:** Lava pools (damage on contact), fire geysers (periodic eruption)
- **Loot Armor:** *Volcanic Scale Mail* — reduces fire damage

| Stage | Content |
|---|---|
| Rooms 1–4 | Procedurally generated rooms with **Race Car Monsters** |
| Mini-Boss Room | **Rock Monster** — a hulking stone golem |
| Rooms 5–7 | Harder rooms with Race Car Monsters + fire hazards |
| Boss Room | **Lava Monster** — guards the **Red Crystal** 🔴 |

**Red Crystal Power:** 🔥 **Fire Breath** — ranged cone attack in the facing direction

### 6.3 Mission 2 — Frost Caves ❄️

- **Theme:** Ice caverns, frozen rivers, crystal stalactites
- **Color Palette:** Light blue, white, dark blue, silver
- **Environmental Hazards:** Ice patches (slippery movement), falling icicles
- **Loot Armor:** *Frostguard Plate* — reduces ice damage

| Stage | Content |
|---|---|
| Rooms 1–4 | Procedurally generated rooms with **Ice Imp Monsters** |
| Mini-Boss Room | **Frost Golem** — a massive ice construct |
| Rooms 5–7 | Harder rooms with Ice Imps + environmental hazards |
| Boss Room | **Blizzard Serpent** — guards the **Blue Crystal** 🔵 |

**Blue Crystal Power:** ❄️ **Ice Blast** — fires a freezing projectile that slows/freezes enemies

### 6.4 Mission 3 — Emerald Marsh 🌿

- **Theme:** Swamp, dense vegetation, poisonous bogs, ruins
- **Color Palette:** Green, dark green, brown, purple (poison)
- **Environmental Hazards:** Poison bogs (DoT on contact), vine traps (snare)
- **Loot Armor:** *Thornweave Armor* — reduces poison damage

| Stage | Content |
|---|---|
| Rooms 1–4 | Procedurally generated rooms with **Swamp Slime Monsters** |
| Mini-Boss Room | **Bog Troll** — a lumbering swamp beast |
| Rooms 5–7 | Harder rooms with Slimes + environmental hazards |
| Boss Room | **Venom Hydra** — guards the **Green Crystal** 🟢 |

**Green Crystal Power:** ☠️ **Poison Cloud** — AoE attack that creates a lingering poison zone

---

## 7. Enemies

### 7.1 Common Mobs (per dungeon)

| Dungeon | Mob Name | Behavior |
|---|---|---|
| Volcano | Race Car Monster | Fast movement, charges at player in straight lines |
| Frost Caves | Ice Imp | Ranged snowball attacks, teleport-dodges when hit |
| Emerald Marsh | Swamp Slime | Slow, splits into 2 smaller slimes when killed |

### 7.2 Mini-Bosses

| Dungeon | Mini-Boss | HP | Pattern |
|---|---|---|---|
| Volcano | Rock Monster | 10 hits | Charges, slams ground (AoE), throws boulders |
| Frost Caves | Frost Golem | 12 hits | Slow punch combos, ice spike ground attack, shield phase |
| Emerald Marsh | Bog Troll | 10 hits | Swipe attacks, pulls player with vines, poison spit |

### 7.3 Final Bosses

| Dungeon | Boss | HP | Pattern |
|---|---|---|---|
| Volcano | Lava Monster | 20 hits | Lava wave attack, fire rain, enrage at 25% HP |
| Frost Caves | Blizzard Serpent | 20 hits | Tail sweep, ice beam, summons ice shards |
| Emerald Marsh | Venom Hydra | 24 hits (3 heads × 8) | Each head attacks independently, poison breath, regenerates heads if not killed fast |

---

## 8. Items & Loot

### 8.1 Health Drops
- **Small Heart:** Restores 1 HP (common drop, ~30% chance from mobs)
- **Large Heart:** Restores 3 HP (rare drop, ~5% chance from mobs, guaranteed from mini-boss)

### 8.2 Armor Sets
| Armor | Found In | Bonus |
|---|---|---|
| Basic Dragon Armor | Starting equipment | No special bonus |
| Volcanic Scale Mail | Dragon Volcano | -50% fire damage taken |
| Frostguard Plate | Frost Caves | -50% ice damage taken |
| Thornweave Armor | Emerald Marsh | -50% poison damage taken |

Armor is found in a treasure chest in a random room within each dungeon.

### 8.3 Crystals (Quest Items)

| Crystal | Unlocks | Description |
|---|---|---|
| 🔴 Red Crystal | Fire Breath | Cone-shaped fire attack (medium range) |
| 🔵 Blue Crystal | Ice Blast | Projectile that freezes enemies for 2 seconds |
| 🟢 Green Crystal | Poison Cloud | AoE pool that deals damage over time for 4 seconds |

---

## 9. Player Mechanics

### 9.1 Health
- **Max HP:** 10 hearts
- **Starting HP:** 10 hearts (full)
- **Damage from mobs:** 1 heart per hit
- **Damage from mini-boss:** 2 hearts per hit
- **Damage from boss:** 3 hearts per hit
- **Environmental damage:** 1 heart per second of contact

### 9.2 Melee Attack
- **Type:** Claw swipe
- **Range:** 1 tile in front of player
- **Damage:** 1 hit per strike
- **Cooldown:** 0.3 seconds

### 9.3 Special Attacks
- **Unlocked by:** Collecting crystals
- **Cooldown:** 2 seconds per use
- **Damage:** 2 hits per use
- **Can cycle between unlocked specials** with number keys (1, 2, 3)

### 9.4 Invincibility Frames
- After taking damage, 1 second of invincibility (player sprite flashes)

---

## 10. Procedural Dungeon Generation

### Algorithm: Graph-Based Room Placement

1. **Generate room graph:** Create a connected graph of N rooms (N = 4 for pre-boss, 3 for post-boss)
2. **Room templates:** Select from a pool of room templates (open arena, corridor, L-shaped, etc.)
3. **Place enemies:** Distribute mob spawns based on room size (2–5 mobs per room)
4. **Place hazards:** Add environmental hazards appropriate to the dungeon theme
5. **Place loot:** One room in each dungeon half contains a treasure chest
6. **Lock doors:** Rooms are locked until all enemies in the current room are defeated
7. **Connect rooms:** Doors on room edges connect to adjacent rooms in the graph

### Room Types (Templates)
- **Arena:** Large open room, enemies spawn in center
- **Corridor:** Long narrow room, enemies patrol back and forth
- **L-Shape:** Right-angle room, enemies hide around corners
- **Pillared Hall:** Open room with obstacle pillars, creates cover
- **Hazard Room:** Fewer enemies but heavy environmental hazards

---

## 11. Save System

### Save Data (JSON)
```json
{
  "character": "russell",
  "crystals_collected": ["red"],
  "current_mission": 2,
  "armor_inventory": ["basic", "volcanic_scale_mail"],
  "equipped_armor": "volcanic_scale_mail",
  "active_special": "fire_breath",
  "play_time_seconds": 3420
}
```

- **Auto-save:** On returning to Dragon Castle after a mission
- **Manual save:** From pause menu while in Dragon Castle
- **Save location:** `~/.dragon_crystal_quest/save.json`
- **Slots:** 3 save slots

---

## 12. UI / HUD

### In-Game HUD
```
┌──────────────────────────────────────────────┐
│ ♥♥♥♥♥♥♥♥♡♡          [🔥 Fire Breath]        │
│                                              │
│                                              │
│                 (Game World)                  │
│                                              │
│                                              │
│                            Mini-Map (corner)  │
└──────────────────────────────────────────────┘
```

- **Top-left:** Heart bar (HP)
- **Top-right:** Active special attack icon + name
- **Bottom-right:** Mini-map showing explored rooms
- **Center:** Game world / action

### Menus
- **Title Screen:** Pixel art logo, animated background, menu options
- **Pause Menu:** Resume, Save (if in castle), Controls, Quit to Title
- **Character Select:** Side-by-side view of Russell and Max with idle animations
- **Mission Board:** Map with mission icons, locked/unlocked status

---

## 13. Art Asset List (for PixelLab.ai)

### Tile Size: 16×16 pixels (standard 8-bit RPG)
### Character Sprite Size: 16×24 pixels
### Resolution: 256×240 native (NES-style), scaled up 3–4× for display

### Asset Categories

**Characters (×2 — Russell & Max):**
- Walk sprites (4 dir × 4 frames = 16 frames)
- Idle sprites (4 dir × 2 frames = 8 frames)
- Attack sprites (4 dir × 3 frames = 12 frames)
- Special attack sprites (4 dir × 3 frames = 12 frames)
- Hurt/Death sprites (6 frames)

**Dragon Castle Tileset:**
- Stone walls, floors, carpets, banners
- Breakfast table with food
- Armor racks (empty and with armor)
- Mission board
- Crystal pedestals (empty and filled ×3 colors)
- Doors, windows, torches

**Volcano Tileset:**
- Rock walls/floors, lava pools, fire geysers
- Stalactites, cracked ground, ember particles

**Frost Caves Tileset:**
- Ice walls/floors, frozen rivers, icicles
- Snow piles, crystal formations, frost particles

**Emerald Marsh Tileset:**
- Swamp ground, water/bog pools, vines/roots
- Dead trees, ruins, mushrooms, poison bubbles

**Enemies (per dungeon — 3 + mini-boss + boss = 5 per dungeon, 15 total):**
- Idle, walk, attack, hurt, death animations for each

**Items:**
- Small heart, large heart
- Treasure chest (closed and open)
- Crystal sprites (red, blue, green) with glow animation
- Armor sprites (4 sets) for inventory display

**UI:**
- Heart icons (full, empty)
- Special attack icons (fire, ice, poison)
- Button prompts
- Menu frames/borders
- Font (8-bit style)

---

## 14. Sound & Music (Stretch Goal)

- **Chiptune music** for: Title screen, Dragon Castle, each dungeon theme, boss battles
- **SFX:** Melee hit, special attack, enemy hit, enemy death, door open, item pickup, crystal collect, player hurt, player death
- **Tools:** Possible free chiptune generators like BeepBox, FamiTracker, or royalty-free 8-bit asset packs

---

## 15. Technical Architecture

### Project Structure
```
DragonGame/
├── main.py                  # Entry point, game loop
├── settings.py              # Constants (screen size, tile size, colors, FPS)
├── requirements.txt         # pygame dependency
│
├── engine/
│   ├── game.py              # Game class (state machine, main loop)
│   ├── camera.py            # Camera follow + viewport
│   ├── input_handler.py     # Input abstraction
│   ├── save_manager.py      # Save/load JSON
│   ├── sound_manager.py     # Audio playback
│   └── asset_loader.py      # Sprite sheet loading & caching
│
├── entities/
│   ├── player.py            # Player class (movement, combat, specials)
│   ├── enemy.py             # Base enemy class
│   ├── mob_volcano.py       # Race Car Monster
│   ├── mob_frost.py         # Ice Imp
│   ├── mob_marsh.py         # Swamp Slime
│   ├── boss_volcano.py      # Rock Monster, Lava Monster
│   ├── boss_frost.py        # Frost Golem, Blizzard Serpent
│   ├── boss_marsh.py        # Bog Troll, Venom Hydra
│   └── npc.py               # Castle NPCs (if any)
│
├── world/
│   ├── dungeon_generator.py # Procedural dungeon builder
│   ├── room.py              # Room class (tiles, enemies, hazards)
│   ├── room_templates.py    # Predefined room layouts
│   ├── tile.py              # Tile class (solid, hazard, etc.)
│   ├── castle.py            # Dragon Castle map
│   └── door.py              # Door / room transition logic
│
├── combat/
│   ├── melee.py             # Melee attack hitbox + logic
│   ├── special_attacks.py   # Fire breath, ice blast, poison cloud
│   ├── projectile.py        # Projectile base class
│   └── damage.py            # Damage calculation + i-frames
│
├── ui/
│   ├── hud.py               # In-game HUD (hearts, special icon)
│   ├── menu.py              # Title screen, pause menu
│   ├── character_select.py  # Character selection screen
│   ├── mission_board.py     # Mission selection UI
│   ├── dialog.py            # Text box / dialog system
│   └── minimap.py           # Dungeon mini-map
│
├── items/
│   ├── item.py              # Base item class
│   ├── heart_drop.py        # Health drop
│   ├── armor.py             # Armor data + equip logic
│   ├── crystal.py           # Crystal quest items
│   └── chest.py             # Treasure chest
│
└── assets/
    ├── sprites/
    │   ├── characters/      # Russell & Max sprite sheets
    │   ├── enemies/         # Enemy sprite sheets (by dungeon)
    │   ├── items/           # Item sprites
    │   ├── tiles/           # Tileset PNGs (castle, volcano, frost, marsh)
    │   └── ui/              # UI elements
    ├── maps/
    │   └── castle.json      # Dragon Castle tile map
    ├── sounds/              # SFX files
    └── music/               # Background music files
```

### Key Technical Details

- **FPS:** 60 (game logic updates at 60 Hz)
- **Native Resolution:** 256×240, rendered to a surface, then scaled 3× to 768×720 window
- **Tile Size:** 16×16 pixels
- **Sprite Groups:** PyGame sprite groups for efficient collision detection and rendering
- **State Machine:** Game states — `TITLE`, `CHARACTER_SELECT`, `CASTLE`, `DUNGEON`, `BOSS`, `PAUSE`, `GAME_OVER`, `VICTORY`
- **Collision:** Axis-aligned bounding box (AABB) for tiles and entities
- **Z-ordering:** Sprites sorted by Y-position for depth (entities behind walls, etc.)

---

## 16. Implementation Phases

### Phase 1 — Foundation 🏗️ ✅ COMPLETE
1. ✅ Set up project structure and PyGame boilerplate
2. ✅ Implement game loop, state machine, and input handler
3. ✅ Create the player entity with 4-directional movement
4. ✅ Implement camera system with player follow
5. ✅ Build tile-based rendering engine
6. ✅ Create placeholder art (colored rectangles)

### Phase 2 — Castle Hub 🏰 ✅ COMPLETE
7. ✅ Design and build Dragon Castle map (handcrafted)
8. ✅ Implement room transitions within the castle
9. ✅ Build the Armory interaction (equip armor)
10. ✅ Build the Mission Board interaction (start mission)
11. ✅ Implement Breakfast Hall (HP restore + opening scene)

### Phase 3 — Combat System ⚔️ ✅ COMPLETE
12. ✅ Implement melee attack with hitbox and cooldown
13. ✅ Create base enemy class with AI state machine (idle, patrol, chase, attack)
14. ✅ Implement damage system with HP and invincibility frames
15. ✅ Add health drop system (enemy loot table)
16. ✅ Implement enemy death and spawn logic

### Phase 4 — Dungeon Generation 🗺️ ✅ COMPLETE
17. ✅ Build procedural room graph generator
18. ✅ Create room templates (arena, corridor, L-shape, etc.)
19. ✅ Implement door/lock system (clear room to unlock)
20. ✅ Add environmental hazards (lava, ice, poison)
21. ✅ Place treasure chests with armor loot

### Phase 5 — Mission 1: Dragon Volcano 🌋
22. Create volcano tileset integration
23. Implement Race Car Monster AI
24. Build Rock Monster (mini-boss) with attack patterns
25. Build Lava Monster (boss) with multi-phase fight
26. Implement Red Crystal reward → Fire Breath unlock

### Phase 6 — Special Attacks & Polish 🔥
27. Implement Fire Breath special attack
28. Build special attack cycling system (1/2/3 keys)
29. Add HUD (heart bar, special attack indicator)
30. Implement mini-map for dungeon navigation

### Phase 7 — Missions 2 & 3 ❄️🌿
31. Frost Caves: tileset, Ice Imp, Frost Golem, Blizzard Serpent, Ice Blast
32. Emerald Marsh: tileset, Swamp Slime, Bog Troll, Venom Hydra, Poison Cloud

### Phase 8 — Menus & Save System 💾
33. Title screen with New Game / Continue / Quit
34. Character select screen
35. Pause menu
36. Save/Load system (3 slots, JSON)
37. Victory screen / end game flow

### Phase 9 — Art & Audio Integration 🎨
38. Replace placeholder art with PixelLab.ai generated assets
39. Integrate chiptune music and SFX
40. Add particle effects (fire embers, ice sparkles, poison bubbles)
41. Add screen transitions (fade in/out between rooms)

### Phase 10 — Testing & Polish 🧪
42. Playtest all three missions end-to-end
43. Balance enemy HP, damage values, drop rates
44. Fix bugs, optimize performance
45. Add juice (screen shake on hits, flash on damage, etc.)

---

## 17. Dependencies

```
pygame>=2.5.0
```

That's it! PyGame handles rendering, input, audio, and basic collision. All game logic is pure Python.

---

## 18. Getting Started (Quick Start)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install pygame

# Run the game
python main.py
```

---

*This document serves as the living design reference for Dragon Crystal Quest. Update it as decisions evolve during development.*
