"""Damage helpers — armor resistance, damage types."""

from enum import Enum
from items.armor import get_armor


class DamageType(Enum):
    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    POISON = "poison"


def apply_armor_resist(raw_damage, armor_id, damage_type):
    """Return effective damage after armor resistance.

    Only elemental damage types are reduced by armor. Physical damage
    passes through at full value.
    """
    if damage_type == DamageType.PHYSICAL:
        return raw_damage

    armor = get_armor(armor_id)
    if armor is None:
        return raw_damage

    resist_map = {
        DamageType.FIRE: armor.fire_resist,
        DamageType.ICE: armor.ice_resist,
        DamageType.POISON: armor.poison_resist,
    }
    resist = resist_map.get(damage_type, 0.0)
    return max(1, int(raw_damage * (1.0 - resist)))
