'''
User controllable player
'''

import pygame
from jackit.core.actor import Actor
from jackit.core.platform import ExitBlock
from jackit.core import CustomEvent

class Player(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine, controls, spawn_point=(0, 0)):
        super(Player, self).__init__(game_engine, 32, 32)
        self.controls = controls
        self.changing_levels = False
        self.rect.x = spawn_point[0]
        self.rect.y = spawn_point[1]

        # TODO: Add stuff like health, items, etc.. to this class

    def collide(self, change_x, change_y, platform):
        '''
        Handle player specific collision events then call base class collide
        '''
        if isinstance(platform, ExitBlock) and not self.changing_levels:
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))
            self.changing_levels = True
        else:
            super(Player, self).collide(change_x, change_y, platform)

    def handle_event(self, event, keys):
        '''
        Handle player events (like controls and stuff)
        @param event - Current event
        @param keys - List of keys currently pressed by key ID
        '''
        if event.type == pygame.KEYUP:
            if event.key == self.controls.left and not keys[self.controls.right]:
                print("Stop going left")
                self.stop()
            elif event.key == self.controls.right and not keys[self.controls.left]:
                print("Stop going right")
                self.stop()
            elif event.key == self.controls.jump:
                print("Stop jumping")
                self.stop_jumping()
        elif event.type == pygame.KEYDOWN:
            if event.key == self.controls.left:
                print("Left key pressed")
                self.go_left()
            elif event.key == self.controls.right:
                print("Right key pressed")
                self.go_right()
            elif event.key == self.controls.jump:
                print("Jump key pressed")
                self.jump()
