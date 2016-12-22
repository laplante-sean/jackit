'''
A block that can be collected
'''

import os
from deploy import SiteDeployment
from jackit.core import BLOCK_WIDTH, BLOCK_HEIGHT
from jackit.core.animation import SpriteStripAnimation
from jackit.core.entity import Entity

class CollectableBlock(Entity):
    '''
    A block that can be collected
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, animation=None):
        super(CollectableBlock, self).__init__(
            game_engine, width, height, x_pos, y_pos, animation=animation)
        self.collectable = True
        self.collideable = False

class Coin(CollectableBlock):
    '''
    Coin worth configurable amount of points
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Coin, self).__init__(game_engine, width, height, x_pos, y_pos)

        self.coin1 = os.path.join(SiteDeployment.resource_path, "sprites", "coin1.bmp")
        self.coin5 = os.path.join(SiteDeployment.resource_path, "sprites", "coin5.bmp")
        self.coin10 = os.path.join(SiteDeployment.resource_path, "sprites", "coin10.bmp")

        self.image.fill((255, 255, 0))
        self._points = 1

    @property
    def points(self):
        '''
        Getter for the _points instance variable
        '''
        return self._points

    @points.setter
    def points(self, value):
        if value == 1:
            self.animation = SpriteStripAnimation(
                self.coin1, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 5, -1, True,
                int(self.game_engine.config.framerate / 7)
            )
        elif value == 5:
            self.animation = SpriteStripAnimation(
                self.coin5, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 7, -1, True,
                int(self.game_engine.config.framerate / 7)
            )
        elif value == 10:
            self.animation = SpriteStripAnimation(
                self.coin10, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 5, -1, True,
                int(self.game_engine.config.framerate / 7)
            )
        else:
            self.image.fill((0, 255, 255))
        self._points = value

class DecryptionKey(CollectableBlock):
    '''
    A block required to unlock a code block
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        key = os.path.join(SiteDeployment.resource_path, "sprites", "key.bmp")

        self.key_animation = SpriteStripAnimation(
            key, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 1, -1)

        super(DecryptionKey, self).__init__(
            game_engine, width, height, x_pos, y_pos, animation=self.key_animation)

        if self.animation is None:
            self.image.fill((200, 200, 200))
