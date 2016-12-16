'''
Enemy behavior functions
'''

import random
from jackit.actors.enemy import Enemy
from jackit.core.physics import Physics

random.seed()

class BasicEnemy(Enemy):
    '''
    Basic enemy turns around on collidion and randomly changes
    direction rarely
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, stats=Physics()):
        super(BasicEnemy, self).__init__(game_engine, width, height, x_pos, y_pos, stats)
        self.random_behavior = False
        self.random_chance = 50

    def update(self):
        super(BasicEnemy, self).update()

        if self.change_x == 0:
            direction = random.randint(Enemy.LEFT, Enemy.RIGHT)
            if direction == Enemy.LEFT:
                self.go_left()
            else:
                self.go_right()

        if self.random_behavior and self.change_x != 0:
            # Low chance of changing direction while moving
            choice = random.randint(0, 50)
            if choice == Enemy.CHANGE_DIR:
                if self.horizontal_movement_action is self.go_left:
                    self.go_right()
                else:
                    self.go_left()

class LedgeSensingEnemy(BasicEnemy):
    '''
    Basic enemy that also turns around on a ledge
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, stats=Physics()):
        super(LedgeSensingEnemy, self).__init__(
            game_engine, width, height,
            x_pos, y_pos, stats
        )

    def update(self):
        super(LedgeSensingEnemy, self).update()

        if self.is_moving_left() and self.is_on_collideable():
            self.rect.y += 2 # Move down 2
            on_ledge = True

            # Check for off ledge while moving left
            for platform in self.game_engine.current_level.platforms:
                if platform.rect.collidepoint(self.rect.left, self.rect.bottom):
                    on_ledge = False
                    break

            self.rect.y -= 2 # Move back up 2

            if on_ledge:
                self.change_x = 0
                self.go_right()

        elif self.is_moving_right() and self.is_on_collideable():
            self.rect.y += 2 # Move down 2
            on_ledge = True

            # Check for off ledge while moving right
            for platform in self.game_engine.current_level.platforms:
                if platform.rect.collidepoint(self.rect.right, self.rect.bottom):
                    on_ledge = False
                    break

            self.rect.y -= 2

            if on_ledge:
                self.change_x = 0
                self.go_left()
