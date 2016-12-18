'''
Enemy behavior functions
'''

import random
from jackit.actors.enemy import Enemy
from jackit.core.physics import Physics
from jackit.core.actor import Actor
from jackit.core.spritegroup import SpriteGroup

random.seed()

class BasicEnemy(Enemy):
    '''
    Basic enemy turns around on collidion and randomly changes
    direction rarely
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos,
                 collides_with=None, stats=Physics()):
        super(BasicEnemy, self).__init__(game_engine, width, height, x_pos, y_pos,
                                         collides_with, stats)
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
    def __init__(self, game_engine, width, height, x_pos, y_pos,
                 collides_with=None, stats=Physics()):
        super(LedgeSensingEnemy, self).__init__(
            game_engine, width, height,
            x_pos, y_pos, collides_with, stats
        )

        # Once a ledge sensing enemy is on a platform it will be there forever
        # Once this is set we stop calling is_on_collideable() b/c we know we are
        self.on_platforms = None

        # Once the enemy has gone back and forth once on a platform these will be known
        # Once known we can further optimize collision by removing every block from
        # the collides_with list except for the player
        self.has_left_ledge = False
        self.has_right_ledge = False

        # True once all optimizations are complete
        self.optimized = False

    def update(self):
        if self.on_platforms is not None:
            self.frame_cache["is_on_collideable"] = self.on_platforms
        if self.has_left_ledge and self.has_right_ledge and not self.optimized:
            self.optimized = True
            actor = None
            for collideable in self.collides_with:
                if isinstance(collideable, Actor): # Find the player and hold onto it
                    actor = collideable
                    break
            self.collides_with = SpriteGroup()
            if actor is not None:
                self.collides_with.add(actor) # Add the player back to the collides_with list
                                              # Now we only check if we collide with one thing
                                              # on each frame

        super(LedgeSensingEnemy, self).update()

        if not self.on_platforms and self.is_on_collideable():
            self.on_platforms = self.frame_cache["is_on_collideable"]

        if self.is_moving_left() and self.on_platforms is not None:
            self.rect.y += 2 # Move down 2
            on_ledge = True

            # Check for off ledge while moving left
            for platform in self.game_engine.current_level.platforms:
                if platform.rect.collidepoint(self.rect.left, self.rect.bottom):
                    on_ledge = False
                    break

            self.rect.y -= 2 # Move back up 2

            if on_ledge:
                self.has_left_ledge = True
                self.change_x = 0
                self.go_right()

        elif self.is_moving_right() and self.on_platforms is not None:
            self.rect.y += 2 # Move down 2
            on_ledge = True

            # Check for off ledge while moving right
            for platform in self.game_engine.current_level.platforms:
                if platform.rect.collidepoint(self.rect.right, self.rect.bottom):
                    on_ledge = False
                    break

            self.rect.y -= 2

            if on_ledge:
                self.has_right_ledge = True
                self.change_x = 0
                self.go_left()
