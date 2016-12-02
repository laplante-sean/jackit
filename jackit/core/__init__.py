'''
Base class for all engine components
'''

import pygame

class EngineComponent:
    '''
    Base class for all engine components
    '''

    def __init__(self, game_engine):
        self.game_engine = game_engine

    def update(self):
        '''
        Update the engine component. Must be implemented
        '''
        raise NotImplementedError()
