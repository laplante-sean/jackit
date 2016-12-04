'''
User controllable player
'''

import pygame
from jackit.core.actor import Actor

class Player(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine, controls):
        super(Player, self).__init__(game_engine, 30, 40)
        self.controls = controls

        # TODO: Add stuff like health, items, etc.. to this class

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
