'''
Global declaration of custom event so everyone has access
'''

import pygame

class CustomEvent:
    '''
    Custom event mapping
    '''
    KILL_SPRITE = pygame.USEREVENT + 0
    EXIT_EDITOR = pygame.USEREVENT + 2
    NEXT_LEVEL = pygame.USEREVENT + 3
    SET_USER = pygame.USEREVENT + 4
    KILL_ENEMY = pygame.USEREVENT + 5


# Global values for block size
BLOCK_WIDTH = 24
BLOCK_HEIGHT = 24
