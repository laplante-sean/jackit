'''
Global declaration of custom event so everyone has access
'''

import pygame

class CustomEvent:
    '''
    Custom event mapping
    '''
    DESPAWN_ENTITY = pygame.USEREVENT + 0
    KILL_ACTOR = pygame.USEREVENT + 1
    EXIT_EDITOR = pygame.USEREVENT + 2
