'''
User controllable player
'''

import pygame
from jackit.core import CustomEvent
from jackit.core.actor import Actor
from jackit.entities import CodeBlock, ExitBlock, DeathBlock

class Player(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine, controls, spawn_point=(0, 0)):
        super(Player, self).__init__(game_engine, 24, 24, spawn_point[0], spawn_point[1])
        self.controls = controls
        self.stats.use_patch = True # Use the UserPatch for player stats

        # Entity() object if the Player is colliding with an interactable block otherwise None
        self.on_interactable_block = None

    def collide(self, change_x, change_y, sprite):
        super(Player, self).collide(change_x, change_y, sprite)

        if isinstance(sprite, CodeBlock):
            self.on_interactable_block = sprite
        elif isinstance(sprite, ExitBlock):
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))
        elif isinstance(sprite, DeathBlock):
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":self}))

    def update(self):
        super(Player, self).update()

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
