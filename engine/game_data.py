"""GameData — progression / profile state separate from the player entity."""

from settings import PLAYER_MAX_HP


class GameData:
    """Tracks all progression state: HP, armor, crystals, missions."""

    def __init__(self):
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.armor_inventory = ["basic"]
        self.equipped_armor = "basic"
        self.crystals_collected = set()
        self.missions_completed = set()
        self.opening_scene_done = False
        self.selected_character = "russell"  # or "max"

    def restore_hp(self):
        self.hp = self.max_hp

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return self.hp <= 0  # returns True if dead

    def collect_crystal(self, crystal_name):
        self.crystals_collected.add(crystal_name)

    def complete_mission(self, mission_id):
        self.missions_completed.add(mission_id)

    def add_armor(self, armor_id):
        if armor_id not in self.armor_inventory:
            self.armor_inventory.append(armor_id)

    def equip_armor(self, armor_id):
        if armor_id in self.armor_inventory:
            self.equipped_armor = armor_id

    def heal(self, amount):
        """Restore HP, clamped to max."""
        self.hp = min(self.max_hp, self.hp + amount)

    def is_mission_unlocked(self, mission_id):
        """Missions unlock sequentially: 1 always available, 2 after mission 1, etc."""
        if mission_id == 1:
            return True
        return (mission_id - 1) in self.missions_completed
