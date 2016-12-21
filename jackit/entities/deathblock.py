'''
A block that kills the player
'''

import os

from deploy import SiteDeployment
from jackit.core import BLOCK_WIDTH, BLOCK_HEIGHT
from jackit.core.entity import Entity
from jackit.core.animation import SpriteStripAnimation

class DeathBlock(Entity):
    '''
    A block that kills the player
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, direction="down"):
        death_block = os.path.join(SiteDeployment.resource_path, "sprites", "death_block.bmp")

        x_mirror = y_mirror = False
        rotation = 0

        if direction == "down":
            y_mirror = True
        elif direction == "left":
            rotation = 90
        elif direction == "right":
            rotation = 270
        elif direction == "up":
            pass
        else:
            pass

        self.db = SpriteStripAnimation(
            death_block, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 1, (0, 149, 255), False,
            int(game_engine.config.framerate / 1), x_mirror=x_mirror, y_mirror=y_mirror,
            rotation=rotation
        )

        super(DeathBlock, self).__init__(
            game_engine, width, height, x_pos, y_pos, animation=self.db)
