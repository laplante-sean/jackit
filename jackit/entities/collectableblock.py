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
