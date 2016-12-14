'''
User controllable player
'''

import pygame
from jackit.core import CustomEvent
from jackit.core.actor import Actor
from jackit.actors.player import Player

class Enemy(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Enemy, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((23, 24, 25))
        self.stats.top_speed = 4
        self.kills_player = True

    def collide(self, change_x, change_y, sprite):
        collideable = super(Enemy, self).collide(change_x, change_y, sprite)

        if collideable and abs(change_x) > 0:
            self.change_x = 1
            self.go_right()

        if isinstance(sprite, Player):
            print("Enemy kills you")
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":sprite}))

        return collideable

    def update(self):
        '''
        Make the enemy move around
        '''
        if self.change_x == 0 and self.change_y == 0:
            self.go_left()

        super(Enemy, self).update()
