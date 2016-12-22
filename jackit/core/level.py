'''
This is a base class for a level. Create child classes
for each level
'''

import pygame

from jackit.core import CustomEvent, BLOCK_WIDTH, BLOCK_HEIGHT
from jackit.actors import LedgeSensingEnemy, BasicEnemy, Player, Enemy
from jackit.core.spritegroup import SpriteGroup
from jackit.core.camera import Camera, complex_camera
from jackit.core.patch import UserPatch
from jackit.entities import Platform, ExitBlock, CodeBlock,\
                            DeathBlock, CollectableBlock,\
                            DecryptionKey, Coin

class LevelGeneratorError(Exception):
    '''
    Error generating the level from the map provided
    '''
    pass

class LevelMap:
    '''
    Level map format characters
    '''
    PLATFORM = "P"
    WALL = "W"
    FLOOR = "F"
    GROUND = "G"
    CLOUD = "C"
    EXIT = "E"
    SPAWN = "S"
    CODE_BLOCK = "c"
    ENCRYPTED_CODE_BLOCK = "X"
    CODE_PLUG = "p"
    DEATH_SPIKE = "D"
    LEFT_DEATH_SPIKE = "<"
    RIGHT_DEATH_SPIKE = ">"
    UP_DEATH_SPIKE = "^"
    BASIC_ENEMY = "B"
    LEDGE_SENSE_ENEMY = "L"
    LEDGE_SENSE_RND_ENEMY = "Z"
    RANDOM_ENEMY = "R"
    MIRROR_ENEMY = "M"
    DECRYPTION_KEY = "K"
    ONE_POINT_COIN = "1"
    FIVE_POINT_COIN = "5"
    TEN_POINT_COIN = "0"

class Level:
    '''
    Base level class. Subclass this to make levels
    '''

    def __init__(self, game_engine, level_map, player):
        self.level_map = level_map
        self.game_engine = game_engine

        # Initialize the entity list
        # This will have all entities for use in collision
        # detection
        self.entities = SpriteGroup()
        self.collideable_entities = SpriteGroup()
        self.interactable_blocks = SpriteGroup()

        # These groups are for draw and update order preservation
        self.platforms = SpriteGroup()
        self.code_blocks = SpriteGroup()
        self.collectable_blocks = SpriteGroup()
        self.enemies = SpriteGroup()
        self.moveable_blocks = SpriteGroup()

        # List of collectable blocks that have been collected so
        # we can put them back on level reset
        self.collected_blocks = SpriteGroup()

        self.width = self.height = 0
        self.death_zone = None
        self.camera = None

        # Init the Player
        self.player = player

    def reset(self):
        '''
        Reset the level
        '''
        # Reset all the sprites
        self.entities.reset()
        self.collected_blocks.reset()

        self.entities.add(self.collected_blocks)
        self.collectable_blocks.add(self.collected_blocks)
        self.collected_blocks.empty()

        # Stop the text editor if it's running
        if self.game_engine.code_editor.is_running():
            self.game_engine.code_editor.stop()

    def unload(self):
        '''
        Unload the level
        '''
        self.width = self.height = 0
        self.death_zone = None
        self.camera = None

        # Empty the lists
        self.platforms.empty()
        self.code_blocks.empty()
        self.collectable_blocks.empty()
        self.collected_blocks.empty()
        self.enemies.empty()
        self.moveable_blocks.empty()
        self.entities.empty()
        self.collideable_entities.empty()
        self.interactable_blocks.empty()

        # Stop the text editor if it's running
        if self.game_engine.code_editor.is_running():
            self.game_engine.code_editor.stop()

    def load(self):
        '''
        Load the level
        '''
        # Build the level from the map
        self.width, self.height = self.build_level()

        # Set up the DEATH ZONE!
        # A rect 50 pixels bigger on all sides than the level
        self.death_zone = pygame.Rect(-50, -50, self.width + 50, self.height + 50)

        # Init the camera
        self.camera = Camera(self.game_engine.screen_size, complex_camera, self.width, self.height)

        # The player collides with everything
        self.player.collides_with = self.entities
        self.entities.add(self.player)

        for enemy in self.enemies:
            enemy.collides_with = SpriteGroup()

            # All enemies need to collide with the player
            enemy.collides_with.add(self.player)

            if not isinstance(enemy, LedgeSensingEnemy):
                for collideable in self.collideable_entities:
                    # All non ledge sensing enemies need only collide with blocks at
                    # their level or below them.
                    if (collideable.rect.y + BLOCK_HEIGHT) > enemy.rect.y:
                        enemy.collides_with.add(collideable)
            else:
                # Ledge sensing enemies need only collide with the player and
                # blocks at their Level (blocks under them is handled bytes
                # sprite.is_on_collideable())
                for collideable in self.collideable_entities:
                    if (collideable.rect.y + (BLOCK_HEIGHT / 2)) > enemy.rect.y and\
                    (collideable.rect.y + (BLOCK_HEIGHT / 2)) < enemy.rect.bottom:
                        enemy.collides_with.add(collideable)

        # Reset the Player
        self.player.reset()

    def build_level(self):
        '''
        Build the level from the map
        '''
        x = y = 0
        for row in self.level_map:
            for col in row:
                sprite = None
                if col == LevelMap.PLATFORM:
                    sprite = self.create_platform(x, y, platform_type="")
                elif col == LevelMap.WALL:
                    sprite = self.create_platform(x, y, platform_type="wall")
                elif col == LevelMap.FLOOR:
                    sprite = self.create_platform(x, y, platform_type="floor")
                elif col == LevelMap.GROUND:
                    sprite = self.create_platform(x, y, platform_type="ground")
                elif col == LevelMap.CLOUD:
                    sprite = self.create_platform(x, y, platform_type="cloud")
                elif col == LevelMap.EXIT:
                    sprite = self.create_exit_block(x, y)
                elif col == LevelMap.SPAWN:
                    self.player.spawn_point = (x, y)
                elif col == LevelMap.CODE_BLOCK:
                    sprite = self.create_platform(x, y, platform_type="code")
                elif col == LevelMap.ENCRYPTED_CODE_BLOCK:
                    sprite = self.create_code_block(x, y, locked=True)
                elif col == LevelMap.CODE_PLUG:
                    sprite = self.create_code_block(x, y)
                elif col == LevelMap.DEATH_SPIKE:
                    sprite = self.create_death_block(x, y)
                elif col == LevelMap.LEFT_DEATH_SPIKE:
                    sprite = self.create_death_block(x, y, direction="left")
                elif col == LevelMap.RIGHT_DEATH_SPIKE:
                    sprite = self.create_death_block(x, y, direction="right")
                elif col == LevelMap.UP_DEATH_SPIKE:
                    sprite = self.create_death_block(x, y, direction="up")
                elif col == LevelMap.BASIC_ENEMY:
                    sprite = self.create_basic_enemy(x, y)
                elif col == LevelMap.LEDGE_SENSE_ENEMY:
                    sprite = self.create_ledge_sense_enemy(x, y)
                elif col == LevelMap.RANDOM_ENEMY:
                    sprite = self.create_random_enemy(x, y)
                elif col == LevelMap.LEDGE_SENSE_RND_ENEMY:
                    sprite = self.create_ledge_sense_random_enemy(x, y)
                elif col == LevelMap.DECRYPTION_KEY:
                    sprite = self.create_decryption_key(x, y)
                elif col == LevelMap.ONE_POINT_COIN:
                    sprite = self.create_coin(x, y, 1)
                elif col == LevelMap.FIVE_POINT_COIN:
                    sprite = self.create_coin(x, y, 5)
                elif col == LevelMap.TEN_POINT_COIN:
                    sprite = self.create_coin(x, y, 10)

                if sprite is not None:
                    if sprite.is_collideable() and not isinstance(sprite, Enemy):
                        self.collideable_entities.add(sprite)
                    elif sprite.is_interactable():
                        self.interactable_blocks.add(sprite)
                    self.entities.add(sprite)

                x += BLOCK_WIDTH
            y += BLOCK_HEIGHT
            x = 0

        total_level_width = len(max(self.level_map, key=len)) * BLOCK_WIDTH
        total_level_height = len(self.level_map) * BLOCK_HEIGHT
        return total_level_width, total_level_height

    def create_coin(self, x_pos, y_pos, value):
        '''
        Create a coin worth value
        '''
        ret = Coin(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos
        )
        ret.points = value
        self.collectable_blocks.add(ret)
        return ret

    def create_decryption_key(self, x_pos, y_pos):
        '''
        Create a collectable adapter plug
        '''
        ret = DecryptionKey(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos
        )
        self.collectable_blocks.add(ret)
        return ret

    def create_random_enemy(self, x_pos, y_pos):
        '''
        Create a random enemy (moves randomly)
        '''
        ret = BasicEnemy(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos
        )
        ret.random_behavior = True
        self.enemies.add(ret)
        return ret

    def create_basic_enemy(self, x_pos, y_pos):
        '''
        Creates a basic enemy
        '''
        ret = BasicEnemy(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos
        )
        self.enemies.add(ret)
        return ret

    def create_ledge_sense_enemy(self, x_pos, y_pos):
        '''
        Creates the ledge sensing enemy
        '''
        ret = LedgeSensingEnemy(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos
        )
        self.enemies.add(ret)
        return ret

    def create_ledge_sense_random_enemy(self, x_pos, y_pos):
        '''
        Creates the ledge sensing enemy with random behavior
        '''
        ret = LedgeSensingEnemy(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos
        )
        ret.random_behavior = True
        self.enemies.add(ret)
        return ret

    def create_code_block(self, x_pos, y_pos, locked=False):
        '''
        Creates a code block. Subclasses can override
        this to assign special functionality to each code block
        '''
        ret = CodeBlock(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos,
            locked=locked
        )
        self.code_blocks.add(ret)
        return ret

    def create_platform(self, x_pos, y_pos, platform_type="ground"):
        '''
        Creates a platform block. Subclasses can override
        this to assign special functionality to each platform block
        '''
        ret = Platform(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos,
            platform_type=platform_type
        )
        self.platforms.add(ret)
        return ret

    def create_exit_block(self, x_pos, y_pos):
        '''
        Creates a exit block. Subclasses can override
        this to assign special functionality to each exit block
        '''
        ret = ExitBlock(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos
        )
        self.platforms.add(ret)
        return ret

    def create_death_block(self, x_pos, y_pos, direction="down"):
        '''
        Creates a block that kills the player on collide
        '''
        ret = DeathBlock(
            self.game_engine,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            x_pos, y_pos,
            direction=direction
        )
        self.platforms.add(ret)
        return ret

    def challenge_completed(self, code_obj):
        '''
        Callback for when user finishes editing the code
        and it passes the compile stage. code_obj can be
        run with exec()
        '''
        return

    def update(self):
        '''
        Update the level
        '''
        # Update the camera to follow the player
        self.camera.update(self.player)

        # Update the player first
        self.player.update()

        # Update all the entities in order
        self.platforms.update()
        self.code_blocks.update()
        self.collectable_blocks.update()
        self.moveable_blocks.update()
        self.enemies.update()

        # Call update complete on all the entities at
        # once becuase order doesn't matter
        self.entities.update_complete()

    def draw(self, screen):
        '''
        Draw all the sprites for the level
        '''

        # Draw the background
        screen.fill((0, 0, 200)) #TODO: Make this a background image of some sort

        # Draw the sprites in proper order so layers look right
        for e in self.platforms:
            screen.blit(e.image, self.camera.apply(e))
        for e in self.code_blocks:
            screen.blit(e.image, self.camera.apply(e))
        for e in self.collectable_blocks:
            screen.blit(e.image, self.camera.apply(e))
        for e in self.moveable_blocks:
            screen.blit(e.image, self.camera.apply(e))
        for e in self.enemies:
            screen.blit(e.image, self.camera.apply(e))

        # Draw the player last
        screen.blit(self.player.image, self.camera.apply(self.player))

    def handle_event(self, event, keys):
        '''
        Handle events for the level
        '''
        if event.type == CustomEvent.KILL_SPRITE:
            if isinstance(event.sprite, Player):
                print("You died")
                self.game_engine.deaths += 1

                # Flash a death frame when they die
                self.game_engine.death_frame.flash()

                # Display you died in the HUD for 2 seconds
                self.game_engine.hud.display_hint("YOU DIED!!", 1)
                self.game_engine.hud.display_hint(
                    "Your code changes persist. Press 'Q' to reset.", 3)

                # Reset the current level. This clears the
                # user patched code
                self.reset()
            elif isinstance(event.sprite, CollectableBlock):
                self.entities.remove(event.sprite)
                self.collectable_blocks.remove(event.sprite)
                self.collected_blocks.add(event.sprite)

                if event.sprite.is_collideable():
                    self.collideable_entities.remove(event.sprite)
                if event.sprite.is_interactable():
                    self.interactable_blocks.remove(event.sprite)
            else:
                event.sprite.reset()
        elif event.type == CustomEvent.EXIT_EDITOR and self.player.is_on_code_block():
            self.player.frame_cache["is_on_code_block"].interaction_complete(event)
        elif event.type == CustomEvent.NEXT_LEVEL:
            self.game_engine.next_level()
            UserPatch.unpatch() # Unpatch the user modification when moving to the next level
            return False # Stop processing more events

        # Don't process controller events for player when code editor is open
        if not self.game_engine.code_editor.is_running():
            # Call to handle event for player
            return self.player.handle_event(event, keys)

        return True # Continue processing events
