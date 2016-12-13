'''
Exit block entity
'''

from jackit.core.entity import Entity

class ExitBlock(Entity):
    '''
    Exit block. Moves to the next level
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(ExitBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((255, 0, 0))
