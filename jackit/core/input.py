'''
Handle user input. Controllers/Mouse/Keyboard
'''

import pygame

from jackit.core import GameComponent

class Input(GameComponent):
    '''
    Handles user input
    '''
    def __init__(self):
        super(Input, self).__init__()
        self.events = pygame.event.get() # Get initial events

    def update(self):
        '''
        Called on each frame. Update user input
        and get events
        '''
        self.events = pygame.event.get()
