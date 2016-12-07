'''
This is a base class for a level. Create child classes
for each level
'''

import pygame

from jackit.core.platform import Platform, ExitBlock
from jackit.core.camera import Camera, complex_camera

class LevelGeneratorError(Exception):
    pass

class LevelMap:
    '''
    Level map format characters
    '''
    PLATFORM = "P"
    EXIT = "E"
    SPAWN = "S"
    CODE = "C"

class Level:
    '''
    Base level class. Subclass this to make levels
    '''

    def __init__(self, game_engine, level_map):
        self.level_map = level_map
        self.game_engine = game_engine

        # Block size for building a level from a map
        self.level_map_block_x = 24
        self.level_map_block_y = 24

        # Spawn point
        self.spawn_point = None

        # Initialize the entity lists
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.entities = pygame.sprite.Group() # List containing all entities

        # Build the level from the map
        self.width, self.height = self.build_level()

        # Update entities
        self.entities.add(self.platform_list, self.enemy_list, self.item_list)

        # Init the camera
        self.camera = Camera(self.game_engine.screen_size, complex_camera, self.width, self.height)

    def build_level(self):
        '''
        Build the level from the map
        '''
        x = y = 0
        for row in self.level_map:
            for col in row:
                if col == LevelMap.PLATFORM:
                    self.platform_list.add(
                        Platform(
                            self.game_engine,
                            self.level_map_block_x,
                            self.level_map_block_y,
                            x, y
                        )
                    )
                elif col == LevelMap.EXIT:
                    self.platform_list.add(
                        ExitBlock(
                            self.game_engine,
                            self.level_map_block_x,
                            self.level_map_block_y,
                            x, y
                        )
                    )
                elif col == LevelMap.SPAWN:
                    self.spawn_point = (x, y)
                elif col == LevelMap.CODE:
                    pass # TODO: Code blocks
                x += self.level_map_block_x
            y += self.level_map_block_y
            x = 0

        if not self.spawn_point:
            raise LevelGeneratorError("No spawn point specified in level map")

        total_level_width = len(max(self.level_map, key=len)) * self.level_map_block_x
        total_level_height = len(self.level_map) * self.level_map_block_y
        return total_level_width, total_level_height

    def update(self, player):
        '''
        Update the level
        '''

        # Update the camera
        self.camera.update(player)

        # Update everything else
        self.entities.update()
        player.update()

    def draw(self, screen, player):
        '''
        Draw all the sprites for the level
        '''

        # Draw the background
        screen.fill((0, 0, 255)) #TODO: Make this a background image of some sort

        # Draw the sprites
        for e in self.entities:
            screen.blit(e.image, self.camera.apply(e))

        screen.blit(player.image, self.camera.apply(player))
