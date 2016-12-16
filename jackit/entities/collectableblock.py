'''
A block that can be collected
'''

from jackit.core.entity import Entity

class CollectableBlock(Entity):
    '''
    A block that can be collected
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(CollectableBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((255, 255, 0))
        self.collectable = True
        self.collideable = False

class Coin(CollectableBlock):
    '''
    Coin worth configurable amount of points
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Coin, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((12, 12, 12))
        self.points = 1

class DecryptionKey(CollectableBlock):
    '''
    A block required to unlock a code block
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(DecryptionKey, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((200, 200, 200))

class OneUp(CollectableBlock):
    '''
    A block that gives the player another life
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(OneUp, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((255, 110, 255))
