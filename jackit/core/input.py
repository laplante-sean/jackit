'''
Handle user input. Controllers/Mouse/Keyboard
'''

import pygame

from jackit.core import EngineComponent

class Input(EngineComponent):
    '''
    Handles user input
    '''
    def __init__(self, game_engine):
        super(Input, self).__init__(game_engine)
        self.events = pygame.event.get() # Get initial events

    def update(self):
        '''
        Called on each frame. Update user input
        and get events
        '''
        self.events = pygame.event.get()
