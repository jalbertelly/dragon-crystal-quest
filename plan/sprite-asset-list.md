# 🐉 Dragon Crystal Quest — Sprite Asset List

> **Art Style:** 8-bit pixel art (NES-era)
> **Native Resolution:** 256×240, scaled 3× for display
> **Tool:** PixelLab.ai (or equivalent pixel art generator)

---

## 1. Playable Characters

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 1 | Russell Idle | 16×24 | Red dragon with crimson scales, standing still, subtle breathing motion | 4 (up/down/left/right) | 2 | Loop | Palette: reds, orange highlights, yellow belly |
| 2 | Russell Walk | 16×24 | Red dragon walking, legs moving, tail swaying | 4 | 4 | Loop | Smooth stride cycle |
| 3 | Russell Melee Attack | 16×24 | Red dragon swiping claws forward, arm extended | 4 | 3 | One-shot | Claw swipe arc visible; frame 2 is the hit frame |
| 4 | Russell Special Attack | 16×24 | Red dragon rearing back and unleashing a special power (mouth open, glowing) | 4 | 3 | One-shot | Generic pose — effect sprites are separate |
| 5 | Russell Hurt | 16×24 | Red dragon recoiling from a hit, flinching backward | 1 (facing camera) | 2 | One-shot | Used during i-frames alongside flashing |
| 6 | Russell Death | 16×24 | Red dragon collapsing to the ground | 1 (facing camera) | 4 | One-shot | Final frame is the dragon flat on the ground |
| 7 | Max Idle | 16×24 | Teal dragon with cool blue-green scales, standing still, subtle breathing | 4 | 2 | Loop | Palette: teals, cyan highlights, light belly |
| 8 | Max Walk | 16×24 | Teal dragon walking, legs moving, tail swaying | 4 | 4 | Loop | Same pose structure as Russell, different palette |
| 9 | Max Melee Attack | 16×24 | Teal dragon swiping claws forward | 4 | 3 | One-shot | Mirror of Russell attack with teal palette |
| 10 | Max Special Attack | 16×24 | Teal dragon rearing back and unleashing a special power | 4 | 3 | One-shot | Same structure as Russell special |
| 11 | Max Hurt | 16×24 | Teal dragon recoiling from a hit | 1 | 2 | One-shot | Teal palette version of Russell hurt |
| 12 | Max Death | 16×24 | Teal dragon collapsing to the ground | 1 | 4 | One-shot | Teal palette version of Russell death |

**Total character frames:** 2 characters × (8 + 16 + 12 + 12 + 2 + 4) = **108 frames**

---

## 2. Enemies — Dragon Volcano 🌋

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 13 | Race Car Monster Idle | 16×16 | A small, wheeled monster with a car-like body, exhaust pipes, and angry eyes; resting | 4 | 2 | Loop | Palette: metallic gray, red accents, black tires |
| 14 | Race Car Monster Walk | 16×16 | Race Car Monster rolling forward, wheels spinning | 4 | 4 | Loop | Fast-moving mob — wheels should blur at speed |
| 15 | Race Car Monster Attack | 16×16 | Race Car Monster charging with a burst of speed, sparks flying | 4 | 3 | One-shot | Charge attack — leaning forward aggressively |
| 16 | Race Car Monster Hurt | 16×16 | Race Car Monster jolted, body tilted, sparks | 1 | 2 | One-shot | Flash white on hit frame |
| 17 | Race Car Monster Death | 16×16 | Race Car Monster exploding into parts, wheels flying off | 1 | 4 | One-shot | Satisfying destruction; final frame is debris |
| 18 | Rock Monster Idle | 24×24 | A hulking stone golem made of volcanic rock, glowing lava cracks, massive fists | 4 | 2 | Loop | Mini-boss; palette: dark gray, orange lava veins |
| 19 | Rock Monster Walk | 24×24 | Rock Monster lumbering forward, heavy footsteps | 4 | 4 | Loop | Slow, heavy movement — ground-shaking feel |
| 20 | Rock Monster Attack | 24×24 | Rock Monster slamming fists into the ground, shockwave | 4 | 4 | One-shot | AoE slam; frame 3 is impact with ground crack |
| 21 | Rock Monster Hurt | 24×24 | Rock Monster staggering, chunks of rock breaking off | 1 | 2 | One-shot | Cracks widen on body |
| 22 | Rock Monster Death | 24×24 | Rock Monster crumbling apart into boulders | 1 | 5 | One-shot | Dramatic collapse into rubble pile |
| 23 | Lava Monster Idle | 32×32 | A massive creature made of molten lava, dripping magma, fiery eyes, towering | 4 | 3 | Loop | Boss; palette: bright orange, red, yellow, black crust |
| 24 | Lava Monster Walk | 32×32 | Lava Monster flowing/sliding forward, leaving a trail of heat | 4 | 4 | Loop | Fluid, molten movement |
| 25 | Lava Monster Attack | 32×32 | Lava Monster raising arms to create a lava wave | 4 | 4 | One-shot | Lava wave attack; also used for fire rain windup |
| 26 | Lava Monster Enrage | 32×32 | Lava Monster glowing brighter, body expanding, flames erupting | 1 | 3 | One-shot | Triggered at 25% HP — visual intensity increase |
| 27 | Lava Monster Hurt | 32×32 | Lava Monster flinching, lava surface rippling | 1 | 2 | One-shot | Crust reforms briefly |
| 28 | Lava Monster Death | 32×32 | Lava Monster cooling and solidifying, cracking apart | 1 | 6 | One-shot | Turns to dark rock, then shatters |

---

## 3. Enemies — Frost Caves ❄️

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 29 | Ice Imp Idle | 16×16 | A small mischievous ice creature, crystalline body, glowing blue eyes, pointy ears | 4 | 2 | Loop | Palette: light blue, white, dark blue accents |
| 30 | Ice Imp Walk | 16×16 | Ice Imp hopping/skittering across ice | 4 | 4 | Loop | Quick, jittery movement |
| 31 | Ice Imp Attack | 16×16 | Ice Imp throwing a snowball, arm extended | 4 | 3 | One-shot | Ranged attack — snowball is a separate projectile sprite |
| 32 | Ice Imp Teleport | 16×16 | Ice Imp dissolving into ice crystals and reforming | 1 | 4 | One-shot | Dodge ability — used when hit |
| 33 | Ice Imp Hurt | 16×16 | Ice Imp knocked back, ice chips flying | 1 | 2 | One-shot | |
| 34 | Ice Imp Death | 16×16 | Ice Imp shattering into ice shards | 1 | 4 | One-shot | Crystalline explosion |
| 35 | Frost Golem Idle | 24×24 | A massive ice construct, blocky body, icicle crown, frosty aura | 4 | 2 | Loop | Mini-boss; palette: icy blue, silver, white |
| 36 | Frost Golem Walk | 24×24 | Frost Golem stomping forward, ice forming under feet | 4 | 4 | Loop | Heavy, deliberate movement |
| 37 | Frost Golem Attack | 24×24 | Frost Golem punching forward, ice spikes erupting from ground | 4 | 4 | One-shot | Combo punch + ground spike |
| 38 | Frost Golem Shield | 24×24 | Frost Golem crossing arms, ice barrier forming around body | 1 | 3 | One-shot | Shield phase — takes reduced damage |
| 39 | Frost Golem Hurt | 24×24 | Frost Golem cracking, ice chunks falling | 1 | 2 | One-shot | |
| 40 | Frost Golem Death | 24×24 | Frost Golem collapsing into an ice pile | 1 | 5 | One-shot | Melts and shatters |
| 41 | Blizzard Serpent Idle | 32×32 | A coiled ice serpent with crystalline scales, cold breath mist, piercing blue eyes | 4 | 3 | Loop | Boss; palette: dark blue, ice white, silver |
| 42 | Blizzard Serpent Move | 32×32 | Blizzard Serpent slithering, body coiling and uncoiling | 4 | 4 | Loop | Sinuous, flowing movement |
| 43 | Blizzard Serpent Attack | 32×32 | Blizzard Serpent lunging with tail sweep or ice beam from mouth | 4 | 4 | One-shot | Tail sweep and ice beam share windup |
| 44 | Blizzard Serpent Summon | 32×32 | Blizzard Serpent rearing up, ice shards forming around it | 1 | 3 | One-shot | Summons ice shard projectiles |
| 45 | Blizzard Serpent Hurt | 32×32 | Blizzard Serpent recoiling, scales cracking | 1 | 2 | One-shot | |
| 46 | Blizzard Serpent Death | 32×32 | Blizzard Serpent freezing solid and shattering | 1 | 6 | One-shot | Dramatic crystallization then explosion |

---

## 4. Enemies — Emerald Marsh 🌿

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 47 | Swamp Slime Idle | 16×16 | A green gelatinous blob with bubbling surface, two beady eyes | 4 | 2 | Loop | Palette: green, dark green, yellow-green highlights |
| 48 | Swamp Slime Walk | 16×16 | Swamp Slime oozing forward, body stretching and squishing | 4 | 4 | Loop | Slow, blobby movement |
| 49 | Swamp Slime Attack | 16×16 | Swamp Slime lunging forward, body extending | 4 | 3 | One-shot | Contact damage on lunge |
| 50 | Swamp Slime Hurt | 16×16 | Swamp Slime compressed on impact, rippling | 1 | 2 | One-shot | |
| 51 | Swamp Slime Death | 16×16 | Swamp Slime splitting into two smaller blobs | 1 | 4 | One-shot | Splits into 2 mini-slimes on death |
| 52 | Mini Slime Idle | 10×10 | A tiny green slime, single eye, jiggling | 4 | 2 | Loop | Spawned when large slime dies |
| 53 | Mini Slime Walk | 10×10 | Mini slime bouncing forward | 4 | 3 | Loop | Faster than parent slime |
| 54 | Mini Slime Death | 10×10 | Mini slime popping into green splash | 1 | 3 | One-shot | Simple pop effect |
| 55 | Bog Troll Idle | 24×24 | A lumbering swamp beast, mossy skin, long vine-like arms, tusks | 4 | 2 | Loop | Mini-boss; palette: dark green, brown, purple accents |
| 56 | Bog Troll Walk | 24×24 | Bog Troll trudging through swamp, heavy steps | 4 | 4 | Loop | Slow, powerful movement |
| 57 | Bog Troll Attack | 24×24 | Bog Troll swiping with long arms or spitting poison | 4 | 4 | One-shot | Swipe + vine pull + poison spit variations |
| 58 | Bog Troll Hurt | 24×24 | Bog Troll staggering, moss falling off | 1 | 2 | One-shot | |
| 59 | Bog Troll Death | 24×24 | Bog Troll sinking into the swamp | 1 | 5 | One-shot | Slowly sinks and dissolves |
| 60 | Venom Hydra Idle | 32×32 | A three-headed serpentine hydra, each head dripping poison, dark purple-green body | 4 | 3 | Loop | Boss; palette: dark green, purple, toxic yellow |
| 61 | Venom Hydra Move | 32×32 | Venom Hydra slithering forward, heads weaving | 4 | 4 | Loop | Each head moves semi-independently |
| 62 | Venom Hydra Attack | 32×32 | Venom Hydra heads lunging and breathing poison | 4 | 4 | One-shot | Multiple heads attack simultaneously |
| 63 | Venom Hydra Regen | 32×32 | Venom Hydra regrowing a severed head, stump glowing | 1 | 4 | One-shot | Head regeneration — stump sprouts new head |
| 64 | Venom Hydra Hurt | 32×32 | Venom Hydra recoiling, one head flinching | 1 | 2 | One-shot | |
| 65 | Venom Hydra Death | 32×32 | Venom Hydra all heads collapsing, body dissolving into toxic pool | 1 | 6 | One-shot | Dramatic poison pool left behind |

---

## 5. Tilesets

| # | Sprite Name | Size (px) | Description | Directions | Variants | Notes |
|---|-------------|-----------|-------------|------------|----------|-------|
| 66 | Castle Stone Wall | 16×16 | Gray stone brick wall with mortar lines | None | 3 | Variations for visual variety |
| 67 | Castle Stone Floor | 16×16 | Polished stone floor tile | None | 2 | Alternating checkerboard pattern |
| 68 | Castle Carpet | 16×16 | Red royal carpet with gold trim | None | 2 | Center and edge variants |
| 69 | Castle Door | 16×16 | Wooden door with iron bands and handle | None | 2 | Open and closed states |
| 70 | Castle Banner | 16×16 | Red banner with dragon emblem hanging on wall | None | 2 | Left-facing and right-facing |
| 71 | Castle Torch | 16×16 | Wall-mounted torch with flickering flame | None | 3 | Animation frames for flame flicker |
| 72 | Castle Window | 16×16 | Arched stone window with light streaming in | None | 1 | |
| 73 | Breakfast Table | 16×16 | Wooden table with plates of food (roasted meat, bread, goblets) | None | 2 | With food and empty |
| 74 | Armor Rack | 16×16 | Wooden rack displaying a suit of armor | None | 5 | Empty, basic, volcanic, frostguard, thornweave |
| 75 | Mission Board | 16×16 | Large wall-mounted map with pins and quest markers | None | 1 | Shows dungeon locations |
| 76 | Crystal Pedestal Empty | 16×16 | Stone pedestal with an empty socket on top | None | 1 | |
| 77 | Crystal Pedestal Red | 16×16 | Stone pedestal with glowing red crystal | None | 3 | Glow animation frames |
| 78 | Crystal Pedestal Blue | 16×16 | Stone pedestal with glowing blue crystal | None | 3 | Glow animation frames |
| 79 | Crystal Pedestal Green | 16×16 | Stone pedestal with glowing green crystal | None | 3 | Glow animation frames |
| 80 | Volcano Rock Wall | 16×16 | Dark volcanic rock with jagged edges, lava veins | None | 3 | Palette: dark brown, black, orange veins |
| 81 | Volcano Rock Floor | 16×16 | Cracked volcanic stone floor, warm tones | None | 2 | Alternating variants |
| 82 | Volcano Lava Pool | 16×16 | Bubbling lava surface, bright orange-yellow | None | 3 | Animation frames for bubbling; environmental hazard |
| 83 | Volcano Fire Geyser | 16×16 | Floor vent that erupts fire periodically | None | 4 | Dormant, rumble, eruption, cooldown; hazard |
| 84 | Volcano Stalactite | 16×16 | Hanging rock formation from ceiling | None | 2 | Intact and broken variants |
| 85 | Volcano Cracked Ground | 16×16 | Fractured stone with ember glow underneath | None | 2 | |
| 86 | Frost Cave Ice Wall | 16×16 | Blue-white ice wall with crystalline facets | None | 3 | Palette: light blue, white, dark blue |
| 87 | Frost Cave Ice Floor | 16×16 | Slippery ice floor, reflective surface | None | 2 | Alternating variants; slippery movement zone |
| 88 | Frost Cave Frozen River | 16×16 | Frozen water surface with cracks | None | 2 | |
| 89 | Frost Cave Icicle | 16×16 | Hanging icicle from ceiling, sharp point | None | 3 | Intact, cracking, falling; hazard |
| 90 | Frost Cave Snow Pile | 16×16 | Mound of snow on the ground | None | 2 | |
| 91 | Frost Cave Crystal Formation | 16×16 | Natural ice crystal cluster growing from floor | None | 2 | Decorative; palette: silver, pale blue |
| 92 | Marsh Swamp Ground | 16×16 | Wet muddy ground with patches of moss | None | 3 | Palette: dark green, brown, olive |
| 93 | Marsh Poison Bog | 16×16 | Bubbling purple-green toxic pool | None | 3 | Animation frames for bubbling; DoT hazard |
| 94 | Marsh Water Pool | 16×16 | Murky swamp water with lily pads | None | 2 | |
| 95 | Marsh Vines | 16×16 | Tangled vines and roots across the ground | None | 2 | Vine trap variant that snares player |
| 96 | Marsh Dead Tree | 16×16 | Gnarled leafless tree trunk | None | 2 | Decorative |
| 97 | Marsh Ruins | 16×16 | Crumbling stone ruins overgrown with moss | None | 3 | Column, wall fragment, arch variants |
| 98 | Marsh Mushroom | 16×16 | Glowing poisonous mushroom cluster | None | 2 | Palette: purple cap, green spots |
| 99 | Marsh Poison Bubbles | 16×16 | Floating poison bubbles above bog surface | None | 3 | Animation frames; particle overlay |

---

## 6. Items & Pickups

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 100 | Small Heart | 8×8 | Small pink-red heart, restores 1 HP | None | 2 | Loop | Gentle pulse/bob animation |
| 101 | Large Heart | 10×10 | Large bright red heart, restores 3 HP | None | 2 | Loop | Brighter and slightly larger than small heart |
| 102 | Treasure Chest Closed | 16×16 | Wooden chest with iron bands, locked/closed | None | 1 | Static | Brown wood, gold latch |
| 103 | Treasure Chest Open | 16×16 | Same chest with lid open, golden glow inside | None | 3 | One-shot | Opening animation: closed → cracking → open with glow |
| 104 | Red Crystal | 16×16 | Glowing red gemstone, faceted, floating | None | 4 | Loop | Floating bob + red glow pulse; quest item |
| 105 | Blue Crystal | 16×16 | Glowing blue gemstone, faceted, floating | None | 4 | Loop | Floating bob + blue glow pulse; quest item |
| 106 | Green Crystal | 16×16 | Glowing green gemstone, faceted, floating | None | 4 | Loop | Floating bob + green glow pulse; quest item |

---

## 7. Armor (Inventory Display)

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 107 | Basic Dragon Armor | 16×24 | Simple leather/scale armor, neutral brown tones | None | 1 | Static | Shown on armor rack and in equip UI |
| 108 | Volcanic Scale Mail | 16×24 | Heavy armor with lava-red scales, glowing orange seams | None | 1 | Static | -50% fire damage; fiery appearance |
| 109 | Frostguard Plate | 16×24 | Icy blue plate armor with frost crystals, silver trim | None | 1 | Static | -50% ice damage; frozen/crystalline look |
| 110 | Thornweave Armor | 16×24 | Woven vine armor with thorns, deep green with purple accents | None | 1 | Static | -50% poison damage; organic/natural look |

---

## 8. Special Attack Effects

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 111 | Fire Breath Effect | 32×16 | Cone-shaped fire blast, flames spreading outward | 4 | 4 | One-shot | Originates from player mouth; palette: orange, yellow, red |
| 112 | Ice Blast Projectile | 8×8 | Spinning ice crystal projectile flying through air | 4 | 3 | Loop | Travels in a straight line; trail of frost particles |
| 113 | Ice Blast Impact | 16×16 | Ice explosion on contact, shards flying outward | None | 4 | One-shot | Freeze effect on enemy |
| 114 | Poison Cloud Effect | 24×24 | Expanding cloud of toxic green-purple gas | None | 5 | One-shot | AoE zone; lingers for 4 seconds then dissipates |
| 115 | Melee Claw Swipe | 16×16 | Arc of claw scratch marks in the air | 4 | 2 | One-shot | Brief slash effect in front of player |
| 116 | Snowball Projectile | 6×6 | Small white snowball in flight | 4 | 2 | Loop | Used by Ice Imp ranged attack |
| 117 | Poison Spit Projectile | 6×6 | Green-purple glob of poison in flight | 4 | 2 | Loop | Used by Bog Troll |
| 118 | Boulder Projectile | 10×10 | Thrown rock/boulder spinning in air | 4 | 3 | Loop | Used by Rock Monster |
| 119 | Ice Shard Projectile | 8×8 | Sharp ice shard flying through air | 4 | 2 | Loop | Summoned by Blizzard Serpent |

---

## 9. Particle Effects

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 120 | Fire Ember | 4×4 | Small orange-red spark floating upward | None | 3 | Loop | Volcano ambient particle |
| 121 | Ice Sparkle | 4×4 | Tiny white-blue glint, twinkling | None | 3 | Loop | Frost Caves ambient particle |
| 122 | Poison Bubble | 4×4 | Small green bubble rising and popping | None | 4 | One-shot | Emerald Marsh ambient particle |
| 123 | Damage Number | 8×8 | Floating number "1", "2", "3" in white/red | None | 1 per digit | Static | Pops up on damage; optional juice |
| 124 | Hit Spark | 8×8 | White-yellow impact spark burst | None | 3 | One-shot | Plays on melee hit contact |
| 125 | Heal Sparkle | 8×8 | Green-white rising sparkle effect | None | 4 | One-shot | Plays when picking up a heart |

---

## 10. UI Elements

| # | Sprite Name | Size (px) | Description | Directions | Frames | Animation | Notes |
|---|-------------|-----------|-------------|------------|--------|-----------|-------|
| 126 | Heart Full | 8×8 | Solid red heart icon for HUD | None | 1 | Static | HP indicator — filled |
| 127 | Heart Empty | 8×8 | Dark outlined empty heart icon for HUD | None | 1 | Static | HP indicator — lost |
| 128 | Fire Breath Icon | 16×16 | Fire ability icon, flame symbol | None | 1 | Static | Shown in HUD when fire special is active |
| 129 | Ice Blast Icon | 16×16 | Ice ability icon, snowflake/crystal symbol | None | 1 | Static | Shown in HUD when ice special is active |
| 130 | Poison Cloud Icon | 16×16 | Poison ability icon, skull/cloud symbol | None | 1 | Static | Shown in HUD when poison special is active |
| 131 | Menu Border | 8×8 | Decorative border tile for menu frames | None | 4 | Static | Corner, horizontal edge, vertical edge, fill |
| 132 | Menu Cursor | 8×8 | Animated arrow/claw cursor for menu selection | None | 2 | Loop | Points right; gentle pulse animation |
| 133 | Button Prompt Z | 16×8 | "Z" key prompt icon | None | 1 | Static | Shown in tutorials/dialogs |
| 134 | Button Prompt X | 16×8 | "X" key prompt icon | None | 1 | Static | |
| 135 | Button Prompt Enter | 24×8 | "Enter" key prompt icon | None | 1 | Static | |
| 136 | Button Prompt Arrows | 24×8 | Arrow keys prompt icon | None | 1 | Static | |
| 137 | Minimap Room | 4×4 | Small square representing a visited dungeon room | None | 3 | Static | Unvisited, current, visited color variants |
| 138 | Minimap Player Dot | 2×2 | Blinking dot for player position on minimap | None | 2 | Loop | |
| 139 | Game Logo | 128×48 | "Dragon Crystal Quest" pixel art title logo | None | 1 | Static | Title screen centerpiece; dramatic dragon font |
| 140 | Title Background | 256×240 | Animated title screen background with castle silhouette and dragons | None | 3 | Loop | Slow parallax scroll or shimmer effect |

---

## Summary

| Category | Sprite Count | Total Frames (approx) |
|----------|-------------|----------------------|
| Playable Characters | 12 | 108 |
| Volcano Enemies | 16 | 58 |
| Frost Caves Enemies | 18 | 62 |
| Emerald Marsh Enemies | 19 | 65 |
| Tilesets | 34 | ~82 |
| Items & Pickups | 7 | 17 |
| Armor (Inventory) | 4 | 4 |
| Special Attack Effects | 9 | ~29 |
| Particle Effects | 6 | ~18 |
| UI Elements | 15 | ~22 |
| **Total** | **140** | **~465** |
