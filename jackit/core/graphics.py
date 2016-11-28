'''
Handle graphics
'''

import pygame

from jackit.core import GameComponent

class Graphics(GameComponent):
    '''
    Handles graphics
    '''
    def __init__(self, screen_size, fullscreen=False):
        super(Graphics, self).__init__()
        self.screen_size = screen_size
        self.fullscreen = fullscreen

        if self.fullscreen:
            self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(screen_size)

    def update(self):
        '''
        Called on each frame. Update graphics
        '''
        self.screen.fill((0, 0, 0))
        
        pygame.display.flip()
