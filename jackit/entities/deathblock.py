'''
A block that kills the player
'''

import pygame

from jackit.core import CustomEvent
from jackit.actors import Player
from jackit.core.entity import Entity

class DeathBlock(Entity):
    '''
    A block that kills the player
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(DeathBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((25, 100, 35))

    def collide_with(self, actor):
        if isinstance(actor, Player):
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_ACTOR, {"actor":actor}))
