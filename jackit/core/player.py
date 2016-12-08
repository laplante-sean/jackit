'''
User controllable player
'''

import pygame
from jackit.core.actor import Actor

class Player(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine, controls, spawn_point=(0, 0)):
        super(Player, self).__init__(game_engine, 24, 24)
        self.controls = controls
        self.changing_levels = False
        self.rect.x = spawn_point[0]
        self.rect.y = spawn_point[1]

    def handle_event(self, event, keys):
        '''
        Handle player events (like controls and stuff)
        @param event - Current event
        @param keys - List of keys currently pressed by key ID
        '''
        if event.type == pygame.KEYUP:
            if event.key == self.controls.left and not keys[self.controls.right]:
                self.stop()
            elif event.key == self.controls.right and not keys[self.controls.left]:
                self.stop()
            elif event.key == self.controls.jump:
                self.stop_jumping()
        elif event.type == pygame.KEYDOWN:
            if event.key == self.controls.left:
                self.go_left()
            elif event.key == self.controls.right:
                self.go_right()
            elif event.key == self.controls.jump:
                self.jump()
            elif event.key == self.controls.interact and self.on_interactable_block:
                print("Interacting with iteractable block")

                # Stop the player and put them over the interactable object
                self.hard_stop()
                self.rect.left = self.on_interactable_block.rect.left
                self.rect.bottom = self.on_interactable_block.rect.bottom

                # Interact with the object
                self.on_interactable_block.interact()
