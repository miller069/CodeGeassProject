"""
subcharacter.py - Character classes

Different character types that players can choose from
"""

import pygame
from character import Character

class Character1(Character):
    """Scavenger - fast, low defense survivor"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Scavenger"
        self.max_hp = 220
        self.hp = 220
        self.attack = 15
        self.defense = 6
        self.speed = 8

        try:
            self.image = pygame.image.load('../../graphics/characters/scavenger.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=True)

    def special_ability(self):
        """Adrenaline Rush: small heal + speed boost"""
        self.hp = min(self.max_hp, self.hp + 20)
        self.speed += 2

    @staticmethod
    def get_display_name():
        return "Scavenger"

    @staticmethod
    def get_description():
        return "A fast survivor who avoids danger and escapes tight situations."

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/scavenger.png'


class Character2(Character):
    """Soldier - tanky frontline fighter"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Soldier"
        self.max_hp = 350
        self.hp = 350
        self.attack = 25
        self.defense = 15
        self.speed = 5

        try:
            self.image = pygame.image.load('../../graphics/characters/soldier.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=True)

    def special_ability(self):
        """Brace - increase defense"""
        self.defense += 8

    @staticmethod
    def get_display_name():
        return "Soldier"

    @staticmethod
    def get_description():
        return "A heavily armored fighter built to survive hordes."

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/soldier.png'


class Character3(Character):
    """Medic - healer and support"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Medic"
        self.max_hp = 260
        self.hp = 260
        self.attack = 12
        self.defense = 8
        self.speed = 6

        try:
            self.image = pygame.image.load('../../graphics/characters/medic.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=True)

    def special_ability(self):
        """Field Heal - restore HP"""
        self.hp = min(self.max_hp, self.hp + 60)

    @staticmethod
    def get_display_name():
        return "Medic"

    @staticmethod
    def get_description():
        return "A survivor who keeps the team alive with medical skills."

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/medic.png'


class Character4(Character):
    """Hunter - fast, high damage, low defense"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Hunter"
        self.max_hp = 240
        self.hp = 240
        self.attack = 22
        self.defense = 5
        self.speed = 9

        try:
            self.image = pygame.image.load('../../graphics/characters/hunter.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=True)

    def special_ability(self):
        """Focus Shot - increase attack"""
        self.attack += 5

    @staticmethod
    def get_display_name():
        return "Hunter"

    @staticmethod
    def get_description():
        return "A silent killer who relies on speed and precision."

    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/hunter.png'


def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character' and cls.__name__.startswith('Character'):
            character_classes.append(cls)
    return character_classes
