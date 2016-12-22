'''
Enemy actor - Computer controlled
'''

import os
from deploy import SiteDeployment
from jackit.core import BLOCK_WIDTH, BLOCK_HEIGHT
from jackit.core.animation import SpriteStripAnimation
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
                 collides_with=None, stats=Physics()):

        run_virus = os.path.join(SiteDeployment.resource_path, "sprites", "virus.bmp")
        self.run_animation = SpriteStripAnimation(
            run_virus, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 4, (0, 0, 0), True,
            int(game_engine.config.framerate / 10), x_mirror=True
        )

        self.run_left_animation = SpriteStripAnimation(
            run_virus, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 4, (0, 0, 0), True,
            int(game_engine.config.framerate / 10)
        )

        super(Enemy, self).__init__(
            game_engine, width, height, x_pos, y_pos,
            collides_with, stats, animation=self.run_animation)

        if not self.animation:
            self.image.fill((23, 24, 25))

    def go_left(self):
        if self.horizontal_movement_action != self.go_left:
            self.animation = self.run_left_animation.iter()
        super(Enemy, self).go_left()

    def go_right(self):
        if self.horizontal_movement_action != self.go_right:
            self.animation = self.run_animation.iter()
        super(Enemy, self).go_right()
