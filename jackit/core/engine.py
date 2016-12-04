'''
Main game engine
'''
import pygame
from deploy import SiteDeployment

# Import game engine components
from jackit.core.input import Input
from jackit.core.player import Player

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
        self.controls = self.config.controls
        self.clock = pygame.time.Clock() # for framerate control
        self.active_sprite_list = pygame.sprite.Group() # All active sprites
        self.running = True

        # Init Input handler
        self.input = Input(self)
        self.player = Player(self)

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

        # Update all active sprites
        self.active_sprite_list.update()
        self.player.update()

        # ALL CODE FOR DRAWING GOES BELOW HERE

        self.screen.fill((0, 0, 255)) # Black background

        self.active_sprite_list.draw(self.screen) # Draw all active sprites

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
            elif event.type == pygame.KEYUP:
                if event.key == self.controls.left and not keys[self.controls.right]:
                    print("Stop going left")
                    self.player.stop()
                elif event.key == self.controls.right and not keys[self.controls.left]:
                    print("Stop going right")
                    self.player.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == self.controls.left:
                    print("Left key pressed")
                    self.player.go_left()
                elif event.key == self.controls.right:
                    print("Right key pressed")
                    self.player.go_right()
                elif event.key == self.controls.up:
                    print("Up key pressed")
                elif event.key == self.controls.down:
                    print("Down key pressed")
                elif event.key == self.controls.jump:
                    print("Jump key pressed")
                    self.player.jump()

GameEngine = EngineSingleton.instance()
