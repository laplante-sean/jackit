'''
User controllable player
'''

import pygame
from jackit.core.actor import Actor
from jackit.core.entity import ExitBlock
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

        # True if the player is colliding with a block that is interactable
        self.on_interactable_block = None

        # TODO: Add stuff like health, items, etc.. to this class

    def update(self):
        self.on_interactable_block = None # Reset each frame
        super(Player, self).update()

    def collide(self, change_x, change_y, entity):
        '''
        Handle player specific collision events then call base class collide
        '''
        if isinstance(entity, ExitBlock) and not self.changing_levels:
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))
            self.changing_levels = True
        elif entity.is_interactable():
            self.on_interactable_block = entity
            if entity.is_collideable():
                super(Player, self).collide(change_x, change_y, entity)
        elif entity.is_collideable():
            super(Player, self).collide(change_x, change_y, entity)

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
            elif event.key == self.controls.interact and self.on_code_block:
                print("Interacting with code block")

