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
        self.collectable = True
        self.collideable = False

class Coin(CollectableBlock):
    '''
    Coin worth configurable amount of points
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Coin, self).__init__(game_engine, width, height, x_pos, y_pos)
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
            self.image.fill((255, 255, 0))
        elif value == 5:
            self.image.fill((255, 255, 100))
        elif value == 10:
            self.image.fill((255, 255, 200))
        else:
            self.image.fill((0, 255, 255))
        self._points = value

class DecryptionKey(CollectableBlock):
    '''
    A block required to unlock a code block
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(DecryptionKey, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((200, 200, 200))
