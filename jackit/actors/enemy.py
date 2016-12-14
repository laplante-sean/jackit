'''
User controllable player
'''

import random
from jackit.core.actor import Actor

class Enemy(Actor):
    '''
    User controlled player
    '''
    LEFT = 0
    RIGHT = 1
    CHANGE_DIR = 2

    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Enemy, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((23, 24, 25))
        self.stats.top_speed = 4
        random.seed()

    def update(self):
        '''
        Make the enemy move around
        '''
        super(Enemy, self).update()

        if self.change_x == 0:
            direction = random.randint(Enemy.LEFT, Enemy.RIGHT)
            if direction == Enemy.LEFT:
                self.go_left()
            else:
                self.go_right()
        else:
            # Really low chance of changing direction while moving
            choice = random.randint(0, 100)
            if choice == Enemy.CHANGE_DIR:
                if self.horizontal_movement_action is self.go_left:
                    self.go_right()
                else:
                    self.go_left()
