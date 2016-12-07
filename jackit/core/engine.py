'''
Main game engine
'''
import pygame
from deploy import SiteDeployment
from jackit.core import CustomEvent

# Import game engine components
from jackit.core.input import Input
from jackit.core.player import Player
from jackit.levels.level_01 import Level_01
from jackit.levels.level_02 import Level_02


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
        pygame.init()

        self.config = SiteDeployment.config
        self.screen_width = self.config.width
        self.screen_height = self.config.height
        self.screen_size = (self.config.width, self.config.height)
        self.fullscreen = self.config.fullscreen
        self.framerate = self.config.framerate
        self.clock = pygame.time.Clock() # for framerate control
        self.running = True

        # Set the display mode
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

        # Init the levels
        self.levels = [Level_01(self), Level_02(self)]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]

        # Init Input handler
        self.input = Input()

        # Init the player
        self.player = Player(self, self.config.controls, spawn_point=self.current_level.spawn_point)

    def update(self):
        '''
        Updates all game components
        '''

        # Get user input for this frame
        self.input.update()

        # Handle input events
        self.handle_events()

        # Update all sprites for the current level
        self.current_level.update(self.player)

        # ALL CODE FOR DRAWING GOES BELOW HERE

        self.current_level.draw(self.screen, self.player) #Draws entities and player

        # ALL CODE FOR DRAWING GOES ABOVE HERE

        # Maintain framerate
        self.clock.tick(self.framerate)

        # Update the screen with what has been drawn
        pygame.display.flip()

    def handle_events(self):
        '''
        Handle user input events
        '''

        # Get the keys that are currently down
        keys = pygame.key.get_pressed()

        for event in self.input.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == CustomEvent.NEXT_LEVEL:
                if self.current_level_index >= (len(self.levels) - 1):
                    self.running = False
                else:
                    self.current_level_index += 1
                    self.current_level = self.levels[self.current_level_index]
                    self.player.rect.x = self.current_level.spawn_point[0]
                    self.player.rect.y = self.current_level.spawn_point[1]
                    self.player.changing_levels = False

            # Call to handle event for player
            self.player.handle_event(event, keys)

GameEngine = EngineSingleton.instance()
