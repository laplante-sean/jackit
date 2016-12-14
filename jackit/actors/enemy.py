'''
Enemy actor - Computer controlled
'''

from jackit.core.actor import Actor
from jackit.core.physics import Physics

class Enemy(Actor):
    '''
    Computer controlled actor
    '''
    LEFT = 0
    RIGHT = 1
    CHANGE_DIR = 2

    def __init__(self, game_engine, width, height, x_pos, y_pos, stats=Physics()):
        super(Enemy, self).__init__(game_engine, width, height, x_pos, y_pos, stats)
        self.image.fill((23, 24, 25))

    def collide(self, change_x, change_y, sprite):
        if isinstance(sprite, Enemy):
            return False # Override the return for collide if an enemy runs into itself

        return super(Enemy, self).collide(change_x, change_y, sprite)
