"""
character.py - Character classes with inventory

Lab 3 Update: Characters now have inventories using ArrayList!
"""

import pygame
from character import Character


class Scavenger(Character):
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Scavenger"
        self.max_hp = 300
        self.hp = 300
        self.attack = 12
        self.defense = 10
        self.speed = 10
        self.import_player_assets(animate=False)

    @staticmethod
    def get_display_name():
        return "Scavenger"

    @staticmethod
    def get_description():
        return ("The most basic, balanced player. Trained to survive in hostile environments "
                "while keeping the mission in mind; get as much loot as you can carry.")

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/scavenger/down/0.png'

    def special_ability(self):
        return {"ability": "Scavenge", "effect": "loot_speed_boost", "speed_bonus": 6, "duration_s": 5}


class Engineer(Character):
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Engineer"
        self.max_hp = 270
        self.hp = 270
        self.attack = 8
        self.defense = 10
        self.speed = 12
        self.import_player_assets(animate=False)

    @staticmethod
    def get_display_name():
        return "Engineer"

    @staticmethod
    def get_description():
        return ("A former military tech expert that worked on military space stations. "
                "Specialized in systems and repairs.")

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/engineer/down/0.png'

    def special_ability(self):
        return {"ability": "System Override", "effect": "disable_doors_and_devices", "duration_s": 6}


class HeavyMercenary(Character):
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "HeavyMercenary"
        self.max_hp = 400
        self.hp = 400
        self.attack = 20
        self.defense = 15
        self.speed = 6
        self.import_player_assets(animate=False)

    @staticmethod
    def get_display_name():
        return "Heavy Mercenary"

    @staticmethod
    def get_description():
        return "Former military soldier, trained in heavy combat."

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/heavymercenary/down/0.png'

    def special_ability(self):
        return {"ability": "Juggernaut", "effect": "damage_reduction", "reduction_pct": 25, "duration_s": 5}


class ReconPilot(Character):
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "ReconPilot"
        self.max_hp = 250
        self.hp = 250
        self.attack = 10
        self.defense = 8
        self.speed = 18
        self.import_player_assets(animate=False)

    @staticmethod
    def get_display_name():
        return "Recon Pilot"

    @staticmethod
    def get_description():
        return ("Former military starship pilot. Used to scout ahead for the rest of the fleet during the war. "
                "Lost his fleet and now must become a scavenger to survive.")

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/reconpilot/down/0.png'

    def special_ability(self):
        return {"ability": "Thermal Scan", "effect": "reveal_enemies_and_loot", "radius": 250, "duration_s": 3}


def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character':
            character_classes.append(cls)
    return character_classes