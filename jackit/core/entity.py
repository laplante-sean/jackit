'''
Sprites for entities (platforms, items, code blocks, etc.)
'''

from jackit.core.sprite import Sprite

class Entity(Sprite):
    '''
    Represents any entity that is not another player/enemy
    '''

    def __init__(self, game_engine, width, height, x_pos, y_pos,
                 collides_with=None, animation=None):
        super(Entity, self).__init__(game_engine, width, height, x_pos, y_pos,
                                     collides_with, animation=animation)

        # True if an entity is collectable (for points or something)
        self.collectable = False

    def is_collectable(self):
        '''
        Getter for the collectable instance variable
        '''
        return self.collectable
