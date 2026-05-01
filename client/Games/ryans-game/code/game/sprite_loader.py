"""
sprite_loader.py - Unified sprite loading system for characters and NPCs

Handles two sprite organization patterns:
1. Animated: graphics/characters/wizard/down/0.png, down/1.png, etc.
2. Static: graphics/characters/wizard.png (single image for all directions)
"""

import pygame
import os


class SpriteLoader:
    """Handles sprite loading for both characters and NPCs with flexible organization."""

    @staticmethod
    def load_character_sprites(character_name, base_path="../../graphics/characters"):
        return SpriteLoader._load_sprites(character_name, base_path, is_character=True)

    @staticmethod
    def load_enemy_sprites(enemy_name, base_path="../../graphics/enemies"):
        return SpriteLoader._load_sprites(enemy_name, base_path, is_character=False)

    @staticmethod
    def load_npc_sprites(npc_name, base_path="../../graphics/npcs"):
        return SpriteLoader._load_sprites(npc_name, base_path, is_character=False)

    @staticmethod
    def _load_sprites(name, base_path, is_character=True):

        name_lower = name.lower()
        animations = {}

        statuses = [
            "up", "down", "left", "right",
            "up_idle", "down_idle", "left_idle", "right_idle"
        ]

        character_dir = os.path.join(base_path, name_lower)

        print(f"  Checking for animated sprites at: {character_dir}")
        print(f"  Directory exists: {os.path.exists(character_dir)}")

        if os.path.exists(character_dir) and os.path.isdir(character_dir):

            print(f"  Loading animated sprites for {name} from {character_dir}")
            animations = SpriteLoader._load_animated_sprites(character_dir, statuses)

            total_frames = sum(len(frames) for frames in animations.values() if frames)
            print(f"  Total frames loaded: {total_frames}")

        else:

            static_path = os.path.join(base_path, f"{name_lower}.png")

            print(f"  Checking for static sprite at: {static_path}")
            print(f"  File exists: {os.path.exists(static_path)}")

            if os.path.exists(static_path):

                print(f"  Loading static sprite for {name} from {static_path}")
                animations = SpriteLoader._load_static_sprite(static_path, statuses)

            else:

                print(f"  No sprites found for {name}, using default colored rectangles")
                animations = SpriteLoader._create_default_sprites(name, statuses, is_character)

        return animations

    @staticmethod
    def _load_animated_sprites(character_dir, statuses):

        animations = {}

        for status in statuses:

            animations[status] = []

            if "_idle" in status:
                direction = status.replace("_idle", "")
            else:
                direction = status

            sprite_dir = os.path.join(character_dir, direction)

            if os.path.exists(sprite_dir) and os.path.isdir(sprite_dir):

                try:

                    all_files = os.listdir(sprite_dir)
                    png_files = [f for f in all_files if f.lower().endswith(".png")]
                    png_files.sort()

                    print(f"    Loading {direction}: found {len(png_files)} PNG files")

                    for png_file in png_files:

                        try:

                            image_path = os.path.join(sprite_dir, png_file)

                            image = pygame.image.load(image_path).convert_alpha()

                            # ↓↓↓ ADDED LINE TO RESIZE LARGE PNGs ↓↓↓
                            image = pygame.transform.scale(image, (64, 64))

                            animations[status].append(image)

                        except pygame.error as e:
                            print(f"      Error loading {image_path}: {e}")

                except Exception as e:
                    print(f"    Error reading directory {sprite_dir}: {e}")

            if not animations[status]:

                default_sprite = SpriteLoader._create_single_default_sprite(direction)
                animations[status] = [default_sprite]

        return animations

    @staticmethod
    def _load_static_sprite(image_path, statuses):

        animations = {}

        try:

            static_image = pygame.image.load(image_path).convert_alpha()

            for status in statuses:
                animations[status] = [static_image.copy()]

        except pygame.error as e:

            print(f"Error loading static sprite {image_path}: {e}")

            for status in statuses:
                default_sprite = SpriteLoader._create_single_default_sprite("down")
                animations[status] = [default_sprite]

        return animations

    @staticmethod
    def _create_default_sprites(name, statuses, is_character=True):

        animations = {}

        if is_character:

            colors = {
                "wizard": (100, 100, 200),
                "cleric": (200, 200, 100),
                "warrior": (200, 100, 100),
                "rogue": (100, 200, 100),
                "paladin": (200, 150, 100),
                "archer": (150, 200, 150),
            }

            default_color = colors.get(name.lower(), (150, 150, 150))

        else:

            colors = {
                "forest_guard": (0, 100, 0),
                "village_merchant": (100, 100, 200),
                "temple_priest": (200, 200, 200),
                "dungeon_scout": (150, 0, 0),
                "market_vendor": (200, 150, 0),
                "wandering_goblin": (80, 140, 60),
            }

            default_color = colors.get(name.lower(), (100, 100, 100))

        for status in statuses:

            direction = status.replace("_idle", "") if "_idle" in status else status

            sprite = SpriteLoader._create_single_default_sprite(direction, default_color)

            animations[status] = [sprite]

        return animations

    @staticmethod
    def _create_single_default_sprite(direction, color=(100, 100, 100)):

        sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
        sprite.fill(color)

        if direction == "up":
            pygame.draw.polygon(sprite, (255, 255, 255), [(16, 5), (10, 15), (22, 15)])
        elif direction == "down":
            pygame.draw.polygon(sprite, (255, 255, 255), [(16, 27), (10, 17), (22, 17)])
        elif direction == "left":
            pygame.draw.polygon(sprite, (255, 255, 255), [(5, 16), (15, 10), (15, 22)])
        elif direction == "right":
            pygame.draw.polygon(sprite, (255, 255, 255), [(27, 16), (17, 10), (17, 22)])

        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 2)

        return sprite

    @staticmethod
    def get_sprite_info(name, base_path):

        name_lower = name.lower()

        character_dir = os.path.join(base_path, name_lower)
        static_path = os.path.join(base_path, f"{name_lower}.png")

        info = {
            "name": name,
            "type": "none",
            "directories": [],
            "files": [],
        }

        if os.path.exists(character_dir) and os.path.isdir(character_dir):

            info["type"] = "animated"

            for item in os.listdir(character_dir):

                item_path = os.path.join(character_dir, item)

                if os.path.isdir(item_path):

                    png_count = len(
                        [f for f in os.listdir(item_path) if f.lower().endswith(".png")]
                    )

                    info["directories"].append(f"{item} ({png_count} frames)")

        elif os.path.exists(static_path):

            info["type"] = "static"
            info["files"].append(f"{name_lower}.png")

        else:

            info["type"] = "default"

        return info