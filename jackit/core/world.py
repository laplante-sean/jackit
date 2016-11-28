'''
Game world
'''

from jackit.core import GameComponent

class World(GameComponent):
    '''
    Sets up and updates the game world
    '''
    def __init__(self):
        super(World, self).__init__()

    def update(self):
        '''
        Called on each frame. Update world
        '''
        pass
