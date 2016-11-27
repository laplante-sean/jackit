'''
The main game loop
'''

import sys
import pygame

class JackitGame:
    '''
    Jack IT Game class
    '''

    def __init__(self, config):
        self.config = config

    def run(self):
        '''
        Run the game
        '''

        pygame.init()
        size = (self.config.width, self.config.height)

        if self.config.fullscreen:
            screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(size)

        running = True
        while running:
            '''
            Main game loop
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break #Stop processing events

            #Don't waste time doing any more processing just quit
            if not running:
                break

            screen.fill((0, 0, 0)) #For now background is black

            # Last thing to do in the loop. Makes everything we've drawn
            # become visible
            pygame.display.flip()
