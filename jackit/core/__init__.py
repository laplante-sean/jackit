'''
Core game componenet abstract base class
'''

class GameComponent:
    '''
    Abstract base class for a game engine component
    '''
    def __init__(self):
        pass

    def update(self):
        '''
        Called on each frame. Allows components to perform updates
        '''
        raise NotImplementedError()
