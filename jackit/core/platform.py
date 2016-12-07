'''
Sprite for platforms
'''

import pygame

class PlatformStats:
    '''
    Stats for a platform
    '''
    def __init__(self, change_x=0, change_y=0, x_travel_dist=0, y_travel_dist=0, acceleration=0):
        self.change_x = change_x
        self.change_y = change_y
        self.x_travel_dist = x_travel_dist
        self.y_travel_dist = y_travel_dist
        self.acceleration = acceleration

class Platform(pygame.sprite.Sprite):
    '''
    Represents a platform that actors can stand on
    '''

    def __init__(self, game_engine, width, height, x_pos, y_pos, platform_stats=PlatformStats()):
        super(Platform, self).__init__()

        # Store the game engine for access to globals
        self.game_engine = game_engine

        # Movement stats
        self.stats = platform_stats

        # Setup the sprite
        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        # Initial position
        self.rect.x = x_pos
        self.rect.y = y_pos

        # Distance it's traveled since last turn around
        self.cur_x_travel_dist = 0
        self.cur_y_travel_dist = 0

        # Current speed vector
        self.change_x = self.stats.change_x
        self.change_y = self.stats.change_y

    def update(self):
        '''
        Update platform position
        '''
        self.cur_x_travel_dist += abs(self.change_x)
        self.cur_y_travel_dist += abs(self.change_y)

        if self.cur_x_travel_dist >= self.stats.x_travel_dist:
            self.stats.change_x *= -1
            self.change_x = self.stats.change_x
            self.cur_x_travel_dist = 0

        if self.cur_y_travel_dist >= self.stats.y_travel_dist:
            self.stats.change_y *= -1
            self.change_y = self.stats.change_y
            self.cur_y_travel_dist = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y


class ExitBlock(Platform):
    '''
    Exit block. Moves to the next level
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(ExitBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((255, 0, 0))
