'''
Exit block entity
'''

import pygame

from jackit.core import CustomEvent
from jackit.actors import Player
from jackit.core.entity import Entity

class ExitBlock(Entity):
    '''
    Exit block. Moves to the next level
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(ExitBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((255, 0, 0))

    def collide(self, actor):
        if isinstance(actor, Player):
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))
