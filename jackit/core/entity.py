'''
Sprites for entities (platforms, items, code blocks, etc.)
'''

from jackit.core.sprite import Sprite

class Entity(Sprite):
    '''
    Represents any entity that is not another player/enemy
    '''

    # TODO: Take an image/color argument to specify sprite image or color of block
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Entity, self).__init__(game_engine, width, height, x_pos, y_pos)

        # True if an entity is moveable
        self.moveable = False

    def update(self):
        '''
        Update the entity position
        '''
        super(Entity, self).update()

    def is_moveable(self):
        '''
        Getter for the moveable instance variable
        '''
        return self.moveable
