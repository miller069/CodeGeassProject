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
  
        return "../graphics/game characters/pitcher.png"


class Catcher(Character):
    def __init__(self, character_name, ops, average, slugging):
        #super().__init__(pos, groups, obstacle_sprites)

        #self.image = pygame.image.load('../graphics/test/fielder.png').convert_alpha()
        #self.rect = self.image.get_rect(topleft=pos)
        #self.hitbox = self.rect.inflate(0, -26)

        self._character_name = character_name # I dont want player changing the athlets names
        self.__ops = ops
        self.__average = average
        self.__slugging = slugging

    def special_ability(self, steady_hand): #boost pitchers stats temporarily
        self.avg_modifier += steady_hand 
        self.slg_modifier += steady_hand
        return  steady_hand

    @staticmethod
    def get_display_name():
        return "Catcher"

    @staticmethod
    def get_description():
        return "Commands the defense and provides power at the plate"
    
    @staticmethod
    def get_preview_image():
  
        return "../graphics/game characters/hitter.png"

class Coach(Character):
    def __init__(self, character_name, ops_plus, average_plus, slugging_plus):
        #super().__init__(pos, groups, obstacle_sprites)
        
        # TODO: Set character image
        #self.image = pygame.image.load('../graphics/test/coach.png').convert_alpha()
        #self.rect = self.image.get_rect(topleft=pos)
        #self.hitbox = self.rect.inflate(0, -26)
        
        # TODO: Set stats
        self._character_name = character_name
        self.__ops_plus = ops_plus
        self.__average_plus = average_plus
        self.__slugging_plus = slugging_plus
    
    # ### TODO: Uncomment and implement these
    def motivational_speech(self, pitcher):
        pitcher.stamina += 40
        return
    
    def apply_coaching(self,hitter):
        hitter.ops += self.ops_plus
        hitter.average += self.average_plus
        hitter.slugging += self.slugging_plus
        return
    
    @staticmethod
    def get_display_name():
         return "Coach"
    
    @staticmethod
    def get_description():
       return "improves the stats of your batter"
    
    @staticmethod
    def get_preview_image():
        return "../graphics/game characters/coach.png"

class Second_baseman(Character):
    """
    TODO: Implement class
    
    """
    def __init__(self, character_name, ops, slugging, average, pos, groups, obstacle_sprites):
        super().__init__(pos, groups, obstacle_sprites)
        
        # TODO: Set character image
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # TODO: Set stats
        self.character_name = character_name
        self.ops = ops
        self.average = average
        self.slugging = slugging
    

    def special_ability(self, player, hype_man): #boost stamina for entire team
        player.stamina += hype_man
        return

    @staticmethod
    def get_display_name():
         return "Second Baseman"
    
    @staticmethod
    def get_description():
         return "an integral player for your defense as well as a consistent contact hitter on offense"
    
    @staticmethod
    def get_preview_image():
        return "../graphics/game characters/second_baseman.png"

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
