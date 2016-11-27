'''
Main game engine
'''

import pygame

from deploy import SiteDeployment

class EngineComponent:
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

class EngineSingleton:
    '''
    Main game engine. Handles updating game componenents
    '''

    _instance = None

    @classmethod
    def instance(cls):
        '''
        Get instance of EngineSingleton
        '''
        if cls._instance is None:
            cls._instance = EngineSingleton()
            return cls._instance
        return cls._instance

    def __init__(self):
        self.config = SiteDeployment.config
        self.screen_size = (self.config.width, self.config.height)
        self.fullscreen = self.config.fullscreen
        self.framerate = self.config.framerate

    def update(self):
        '''
        Updates the game screen
        '''
        pass


GameEngine = EngineSingleton.instance()
