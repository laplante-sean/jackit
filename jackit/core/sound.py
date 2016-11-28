'''
Handle playing sound
'''

from jackit.core import GameComponent

class Sound(GameComponent):
    '''
    Plays sound
    '''
    def __init__(self):
        super(Sound, self).__init__()

    def update(self):
        '''
        Called on each frame. Update sound output
        '''
        pass
