'''
Handle user input. Controllers/Mouse/Keyboard
'''

import pygame

class Input:
    '''
    Handles user input
    '''
    def __init__(self):
        self.events = pygame.event.get() # Get initial events

    def update(self):
        '''
        Called on each frame. Update user input
        and get events
        '''
        self.events = pygame.event.get()
