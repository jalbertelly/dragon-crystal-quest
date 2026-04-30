"""Armor — armor data definitions and helpers."""

from dataclasses import dataclass


@dataclass
class Armor:
    id: str
    name: str
    description: str
    fire_resist: float = 0.0
    ice_resist: float = 0.0
    poison_resist: float = 0.0


# All armor sets in the game
ARMOR_DATA = {
    "basic": Armor(
        id="basic",
        name="Basic Dragon Armor",
        description="Standard-issue armor. No special bonus.",
    ),
    "volcanic_scale_mail": Armor(
        id="volcanic_scale_mail",
        name="Volcanic Scale Mail",
        description="Forged in dragonfire. -50% fire damage.",
        fire_resist=0.5,
    ),
    "frostguard_plate": Armor(
        id="frostguard_plate",
        name="Frostguard Plate",
        description="Enchanted with ice runes. -50% ice damage.",
        ice_resist=0.5,
    ),
    "thornweave_armor": Armor(
        id="thornweave_armor",
        name="Thornweave Armor",
        description="Woven from marshvine. -50% poison damage.",
        poison_resist=0.5,
    ),
}


def get_armor(armor_id):
    """Return the Armor data for the given ID, or None."""
    return ARMOR_DATA.get(armor_id)


def get_armor_bonus_text(armor_id):
    """Return a short string describing the armor's bonus."""
    armor = get_armor(armor_id)
    if armor is None:
        return ""
    bonuses = []
    if armor.fire_resist > 0:
        bonuses.append(f"-{int(armor.fire_resist * 100)}% fire")
    if armor.ice_resist > 0:
        bonuses.append(f"-{int(armor.ice_resist * 100)}% ice")
    if armor.poison_resist > 0:
        bonuses.append(f"-{int(armor.poison_resist * 100)}% poison")
    return ", ".join(bonuses) if bonuses else "No bonus"
