'''
Platform entity
'''

import os
from deploy import SiteDeployment
from jackit.core import BLOCK_WIDTH, BLOCK_HEIGHT
from jackit.core.entity import Entity
from jackit.core.animation import SpriteStripAnimation

class PlatformStats:
    '''
    Stats for a moving platform
    '''
    def __init__(self, change_x=0, change_y=0, x_travel_dist=0, y_travel_dist=0, acceleration=0):
        self.change_x = change_x
        self.change_y = change_y
        self.x_travel_dist = x_travel_dist
        self.y_travel_dist = y_travel_dist
        self.acceleration = acceleration

class Platform(Entity):
    '''
    Represents a platform that actors can stand on
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos,
                 platform_stats=PlatformStats(), platform_type="ground"):

        ground_path = os.path.join(SiteDeployment.resource_path, "sprites", "ground.bmp")
        floor_path = os.path.join(SiteDeployment.resource_path, "sprites", "floor.bmp")
        cloud_path = os.path.join(SiteDeployment.resource_path, "sprites", "cloud.bmp")
        wall_path = os.path.join(SiteDeployment.resource_path, "sprites", "wall.bmp")

        self.animation = None

        if platform_type == "ground":
            self.animation = SpriteStripAnimation(
                ground_path, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 1)
        elif platform_type == "cloud":
            self.animation = SpriteStripAnimation(
                cloud_path, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 1, (0, 0, 0))
        elif platform_type == "floor":
            self.animation = SpriteStripAnimation(
                floor_path, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 1)
        elif platform_type == "wall":
            self.animation = SpriteStripAnimation(
                wall_path, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 1)

        super(Platform, self).__init__(
            game_engine, width, height, x_pos, y_pos, animation=self.animation)

        if self.animation is None:
            self.image.fill((0, 255, 0)) # Green

        # Movement stats if it's moving platform
        self.stats = platform_stats

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
