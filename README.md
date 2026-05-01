# 🐉 Dragon Crystal Quest

A 2D top-down action RPG built with Python and Pygame, inspired by classic NES titles like *The Legend of Zelda* and *Final Fantasy*.

Play as one of two dragons — **Russell** (Red) or **Max** (Teal) — on an epic quest to retrieve three magical crystals from dangerous, procedurally generated dungeons. Each crystal unlocks a powerful new special attack. Between missions, return to **Dragon Castle** to swap armor and prepare for the next adventure.

## ✨ Features

- **Two playable characters** with unique pixel art sprites (cosmetic choice)
- **Real-time combat** with melee attacks and unlockable special abilities
- **Procedurally generated dungeons** with varied room templates and environmental hazards
- **Three themed missions** — Dragon Volcano 🌋, Frost Caves ❄️, and Emerald Marsh 🌿
- **Boss battles** with multi-phase attack patterns
- **Armor & loot system** with dungeon-specific equipment
- **NES-style pixel art** at 256×240 native resolution, scaled 3× for display
- **Save/load system** with 3 save slots

## 🎮 Controls

| Input | Action |
|---|---|
| Arrow Keys / WASD | Move (4-directional) |
| Z / Space | Melee Attack (claw swipe) |
| X / Left Shift | Special Attack (unlocked via crystals) |
| Enter | Interact / Confirm |
| Escape | Pause Menu |
| 1, 2, 3 | Cycle special attack |

## 🗺️ Game World

### Dragon Castle (Hub)
The home base between missions. Visit the **Breakfast Hall** to restore HP, the **Armory** to equip collected armor, and the **Mission Board** to embark on your next quest. Crystal pedestals track your progress as you collect each crystal.

### Missions

| Mission | Theme | Boss | Crystal Reward |
|---|---|---|---|
| Dragon Volcano 🌋 | Lava, magma, fire geysers | Lava Monster | 🔴 Red Crystal — Fire Breath |
| Frost Caves ❄️ | Ice caverns, frozen rivers | Blizzard Serpent | 🔵 Blue Crystal — Ice Blast |
| Emerald Marsh 🌿 | Swamp, poison bogs, ruins | Venom Hydra | 🟢 Green Crystal — Poison Cloud |

## 🏗️ Project Structure

```
dragon-crystal-quest/
├── main.py                  # Entry point
├── settings.py              # Constants (screen size, tile size, colors, FPS)
├── requirements.txt         # Dependencies
├── engine/                  # Core systems (game loop, camera, input)
├── entities/                # Player, enemies, NPCs
├── world/                   # Dungeon generation, rooms, tiles, hazards
│   ├── dungeon_generator.py # Procedural 9-room dungeon builder
│   ├── room_templates.py    # ASCII room templates (12 variants)
│   └── hazard.py            # Environmental hazard damage tracker
├── combat/                  # Melee, special attacks, damage
├── ui/                      # HUD, menus, dialog
├── items/                   # Armor, crystals, loot drops, chests
│   └── chest.py             # Treasure chest with armor loot
└── assets/                  # Sprites, tilesets, sounds, music
```

## 🚀 Getting Started

### Prerequisites

- Python 3.x

### Installation

```bash
# Clone the repository
git clone https://github.com/jalbertelly/dragon-crystal-quest.git
cd dragon-crystal-quest

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

## 🛠️ Development Status

The game is actively in development. Phases 1–4 are complete:

- **Phase 1 — Foundation:** Game loop, state machine, player movement, camera system, tile-based rendering with placeholder pixel art.
- **Phase 2 — Castle Hub:** Multi-room Dragon Castle with door transitions, Breakfast Hall (HP restore), Armory (equip armor), Mission Board (start quests), and crystal pedestals.
- **Phase 3 — Combat System:** Melee attacks with hitbox and cooldown, enemy AI state machine (idle/patrol/chase/attack), damage system with HP and invincibility frames, health drops from enemies.
- **Phase 4 — Dungeon Generation:** Procedural 9-room dungeons (4 normal → mini-boss → 3 hard → boss), 12 ASCII room templates (arena, corridor, L-shape, pillared, hazard, mini-boss, boss), door/lock system (clear enemies to unlock exit), environmental hazards (lava damage, ice speed-up, poison damage), and treasure chests with mission-specific armor loot.

See [dragon-game-design-plan.md](dragon-game-design-plan.md) for the full design document and implementation roadmap.

## 📦 Dependencies

- [Pygame](https://www.pygame.org/) >= 2.5.0

## 📄 License

See the [LICENSE](LICENSE) file for details.
