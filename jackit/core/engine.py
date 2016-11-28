'''
Main game engine
'''

import os
import sys
import pygame
from deploy import SiteDeployment

# Import game engine components
from jackit.core.graphics import Graphics
from jackit.core.world import World
from jackit.core.sound import Sound
from jackit.core.input import Input

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
        self.clock = pygame.time.Clock() # for framerate control

        # Setup the game engine components

        self.graphics = Graphics(self.screen_size, fullscreen=self.fullscreen)
        self.world = World()
        self.input = Input()
        self.sound = Sound()

        # TODO: Put this in actors.py
        self.ball = pygame.image.load(
            os.path.join(SiteDeployment.resource_path, "sprites", "ball.gif")
        )
        self.ballrect = self.ball.get_rect()
        self.speed = [2, 2]

    def update(self):
        '''
        Updates all game components
        '''
        # Handle events
        self.handle_events()

        # Update Input
        self.input.update()

        # Update World
        self.world.update()

        self.ballrect = self.ballrect.move(self.speed)
        if self.ballrect.left < 0 or self.ballrect.right > self.graphics.screen_size[0]:
            self.speed[0] = -self.speed[0]
        if self.ballrect.top < 0 or self.ballrect.bottom > self.graphics.screen_size[1]:
            self.speed[1] = -self.speed[1]

        self.graphics.screen.blit(self.ball, self.ballrect)

        # Update screen (MUST BE LAST)
        self.graphics.update()

        # Maintain framerate
        self.clock.tick(self.framerate)

    def handle_events(self):
        '''
        Handle input events
        '''
        for event in self.input.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

GameEngine = EngineSingleton.instance()
