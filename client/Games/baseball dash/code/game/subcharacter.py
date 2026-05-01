"""
subcharacter.py - Character classes

Different character types that players can choose from
"""

from operator import pos

import pygame
from character import Character
from inventory import Inventory
from item import create_example_items

class Pitcher(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, character_name="Pitcher", avg_modifier=40, slg_modifier=50, is_local=False):
        super().__init__(pos, groups, obstacle_sprites)
        
        # TODO: Set character image
        self.image = pygame.image.load('../../graphics/characters/pitcher.png').convert_alpha()
        # scale to match other sprites (64x64 is typical)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # TODO: Set stats
        self.character_name = character_name
        self.__avg_modifier = avg_modifier  
        self.__slg_modifier = slg_modifier
        self.is_local = is_local
        self.status = "idle"

        self.inventory = Inventory()

    def reduce_stamina(self, damage):
        self.damage = damage
        self.__stamina -= damage

        if self.__stamina < 0:
            self.__stamina = 0
        return damage
    
    def is_alive(self):
        if self.__stamina <= 0:
            return False
        if self.stamina > 0:
            return True

    def heal(self, amount):
        if self.stamina + amount > 100:
            self.stamina = 100
        else:
            self.stamina += amount

        return amount

    def add_item(self, item):
        self.items.append(item)
        return 
    def special_ability(self, hot_streak): #boost pitchers stats temporarily
        # TODO: Implement special ability
        self.avg_modifier += hot_streak 
        self.slg_modifier += hot_streak
        return 
    
    # ### TODO: Uncomment and implement these
    @staticmethod
    def get_display_name():
        return "Pitcher"
    
    @staticmethod
    def get_description():
         return "An electric young pitcher with high velocity and command"
    
    @staticmethod
    def get_preview_image():
  
        return '../../graphics/characters/pitcher.png'


class Slugger(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, character_name="Slugger", avg_modifier=40, slg_modifier=50, is_local=False):
        super().__init__(pos, groups, obstacle_sprites)
        
        # TODO: Set character image
        self.image = pygame.image.load('../../graphics/characters/slugger.png').convert_alpha()
        # scale to match other sprites (64x64 is typical)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # TODO: Set stats
        self.character_name = character_name
        self.__avg_modifier = avg_modifier  
        self.__slg_modifier = slg_modifier
        self.is_local = is_local
        self.status = "idle"

        self.inventory = Inventory()

    def reduce_stamina(self, damage):
        self.damage = damage
        self.__stamina -= damage

        if self.__stamina < 0:
            self.__stamina = 0
        return damage
    
    def is_alive(self):
        if self.__stamina <= 0:
            return False
        if self.stamina > 0:
            return True

    def heal(self, amount):
        if self.stamina + amount > 100:
            self.stamina = 100
        else:
            self.stamina += amount

        return amount

    def add_item(self, item):
        self.items.append(item)
        return 
    def special_ability(self, hot_streak): #boost pitchers stats temporarily
        # TODO: Implement special ability
        self.avg_modifier += hot_streak 
        self.slg_modifier += hot_streak
        return 
    
    # ### TODO: Uncomment and implement these
    @staticmethod
    def get_display_name():
        return "Slugger"
    
    @staticmethod
    def get_description():
         return "A powerful slugger with exceptional home run potential"
    @staticmethod
    def get_preview_image():
  
        return "../../graphics/characters/slugger.png"

class Coach(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, character_name="Coach", avg_modifier=40, slg_modifier=50, is_local=False):
        super().__init__(pos, groups, obstacle_sprites)
        
        # TODO: Set character image
        self.image = pygame.image.load('../../graphics/characters/coach.png').convert_alpha()
        # scale to match other sprites (64x64 is typical)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # TODO: Set stats
        self.character_name = character_name
        self.__avg_modifier = avg_modifier  
        self.__slg_modifier = slg_modifier
        self.is_local = is_local
        self.status = "idle"

        self.inventory = Inventory()

    def reduce_stamina(self, damage):
        self.damage = damage
        self.__stamina -= damage

        if self.__stamina < 0:
            self.__stamina = 0
        return damage
    
    def is_alive(self):
        if self.__stamina <= 0:
            return False
        if self.stamina > 0:
            return True

    def heal(self, amount):
        if self.stamina + amount > 100:
            self.stamina = 100
        else:
            self.stamina += amount

        return amount

    def add_item(self, item):
        self.items.append(item)
        return 
    def special_ability(self, hot_streak): #boost pitchers stats temporarily
        # TODO: Implement special ability
        self.avg_modifier += hot_streak 
        self.slg_modifier += hot_streak
        return 
    
    # ### TODO: Uncomment and implement these
    @staticmethod
    def get_display_name():
        return "Coach"
    
    @staticmethod
    def get_description():
         return "A powerful coach with exceptional leadership skills"
    @staticmethod
    def get_preview_image():
  
        return "../../graphics/characters/coach.png"

class Second_baseman(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, pos, groups, obstacle_sprites, character_name="Second Baseman", avg_modifier=40, slg_modifier=50, is_local=False):
        super().__init__(pos, groups, obstacle_sprites)
        
        # TODO: Set character image
        self.image = pygame.image.load('../../graphics/characters/second_baseman.png').convert_alpha()
        # scale to match other sprites (64x64 is typical)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # TODO: Set stats
        self.character_name = character_name
        self.__avg_modifier = avg_modifier  
        self.__slg_modifier = slg_modifier
        self.is_local = is_local
        self.status = "idle"

        self.inventory = Inventory()

    def reduce_stamina(self, damage):
        self.damage = damage
        self.__stamina -= damage

        if self.__stamina < 0:
            self.__stamina = 0
        return damage
    
    def is_alive(self):
        if self.__stamina <= 0:
            return False
        if self.stamina > 0:
            return True

    def heal(self, amount):
        if self.stamina + amount > 100:
            self.stamina = 100
        else:
            self.stamina += amount

        return amount

    def add_item(self, item):
        self.items.append(item)
        return 
    def special_ability(self, hot_streak): #boost pitchers stats temporarily
        # TODO: Implement special ability
        self.avg_modifier += hot_streak 
        self.slg_modifier += hot_streak
        return 
    
    # ### TODO: Uncomment and implement these
    @staticmethod
    def get_display_name():
        return "Second Baseman"
    
    @staticmethod
    def get_description():
         return "A skilled second baseman with excellent fielding abilities"
    @staticmethod
    def get_preview_image():
  
        return "../../graphics/characters/second_baseman.png"

# ============================================
# CHARACTER REGISTRY (Auto-discovery)
# ============================================

def get_all_character_classes():
    """
    Automatically discover all character classes
    Returns list of character classes (not instances)
    """
    # Get all subclasses of Character
    character_classes = []
    
    for cls in Character.__subclasses__():
        # Skip the base Character class
        if cls.__name__ != 'Character':
            character_classes.append(cls)
    
    return character_classes
