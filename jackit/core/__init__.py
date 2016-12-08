'''
Global declaration of custom event so everyone has access
'''

import pygame

class CustomEvent:
    '''
    Custom event mapping
    '''
    NEXT_LEVEL = pygame.USEREVENT + 0
    DESPAWN_ENTITY = pygame.USEREVENT + 1
    KILL_ACTOR = pygame.USEREVENT + 2
