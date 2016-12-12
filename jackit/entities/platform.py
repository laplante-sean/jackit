'''
Platform entity
'''

from jackit.core.entity import Entity, EntityStats

class PlatformStats(EntityStats):
    '''
    Stats for a moving platform
    '''
    def __init__(self, change_x=0, change_y=0, x_travel_dist=0, y_travel_dist=0, acceleration=0):
        super(PlatformStats, self).__init__()
        
        self.change_x = change_x
        self.change_y = change_y
        self.x_travel_dist = x_travel_dist
        self.y_travel_dist = y_travel_dist
        self.acceleration = acceleration

class Platform(Entity):
    '''
    Represents a platform that actors can stand on
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, platform_stats=PlatformStats()):
        super(Platform, self).__init__(game_engine, width, height, x_pos, y_pos, platform_stats)

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
