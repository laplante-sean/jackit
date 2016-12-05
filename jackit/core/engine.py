'''
Main game engine
'''
import pygame
from deploy import SiteDeployment

# Import game engine components
from jackit.core.input import Input
from jackit.core.player import Player
from jackit.core.platform import Platform, PlatformStats

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

        # Sprite lists
        self.platform_sprite_list = pygame.sprite.Group()
        self.player_sprite_list = pygame.sprite.Group()
        self.item_sprite_list = pygame.sprite.Group()
        self.enemy_sprite_list = pygame.sprite.Group()

        # Init Input handler
        self.input = Input()

        # Init the player
        self.player = Player(self, self.config.controls)
        self.player_sprite_list.add(self.player)

        # TODO: This is a test platform
        test_platform = Platform(self, 100, 10, 350, 475)
        test_platform_stats = PlatformStats(
            change_x=3,
            change_y=0,
            x_travel_dist=250,
            y_travel_dist=0
        )
        test_platform2 = Platform(self, 150, 10, 475, 430, platform_stats=test_platform_stats)
        self.platform_sprite_list.add(test_platform)
        self.platform_sprite_list.add(test_platform2)

        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

    def update(self):
        '''
        Updates all game components
        '''

        # Get user input for this frame
        self.input.update()

        # Handle input events
        self.handle_events()

        # Update all the sprites (must come after actor updates)
        # Automatically calls each Sprite.update() method
        self.platform_sprite_list.update()
        self.item_sprite_list.update()
        self.enemy_sprite_list.update()
        self.player_sprite_list.update() # Update the player last

        # ALL CODE FOR DRAWING GOES BELOW HERE

        self.screen.fill((0, 0, 255)) # Blue background

        # Draw all active sprites
        self.platform_sprite_list.draw(self.screen)
        self.item_sprite_list.draw(self.screen)
        self.enemy_sprite_list.draw(self.screen)
        self.player_sprite_list.draw(self.screen)

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

            # Call to handle event for player
            self.player.handle_event(event, keys)

GameEngine = EngineSingleton.instance()
