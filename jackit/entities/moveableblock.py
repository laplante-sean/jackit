'''
A block that can be pushed
'''

from jackit.core.entity import Entity

class MoveableBlock(Entity):
    '''
    A block that can be pushed
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(MoveableBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((0, 255, 255))
    