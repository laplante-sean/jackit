'''
Physics for the game
Can be modified on a per entity/actor basis
'''

class Physics:
    '''
    Default physics
    '''
    def __init__(self, gravity=1.05, terminal_velocity=20):

        # Force of gravity
        self.gravity = gravity

        # Maximum object falling speed
        self.terminal_velocity = terminal_velocity
