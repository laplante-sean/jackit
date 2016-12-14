'''
A block that kills the player
'''

from jackit.core.entity import Entity

class DeathBlock(Entity):
    '''
    A block that kills the player
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(DeathBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((25, 100, 35))
