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

    def __init__(self, game_engine, width, height, x_pos, y_pos,
                 collides_with=None, stats=Physics()
                ):
        super(Enemy, self).__init__(game_engine, width, height, x_pos, y_pos, collides_with, stats)
        self.image.fill((23, 24, 25))
