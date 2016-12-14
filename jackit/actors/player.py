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

    def collide(self, change_x, change_y, sprite):
        collideable = super(Player, self).collide(change_x, change_y, sprite)

        if isinstance(sprite, ExitBlock):
            print("Exit block")
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))
        elif isinstance(sprite, DeathBlock):
            print("Death block")
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":self}))
        elif sprite.kills_player:
            print("Enemy block")
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":self}))

        return collideable

    def update(self):
        super(Player, self).update()

    def is_on_code_block(self):
        '''
        True if the Player is on a code block
        Uses frame cache to improve performance
        for subsequent calls
        '''
        if self.frame_cache.get("is_on_code_block", None) is not None:
            return True

        if not self.is_on_interactable():
            return False

        for interactable in self.frame_cache["is_on_interactable"]:
            if isinstance(interactable, CodeBlock):
                self.frame_cache["is_on_code_block"] = interactable
                return True # Level design should only allow player to be on one code block
                            # at a time. If not, too bad, I'm ignoring any others.

        return False

    def is_on_interactable(self):
        '''
        True if Player is on an interactable entity
        uses frame cache to ensure subsequent calls
        are faster
        '''

        # Speed up calls to this method if used more than once per frame
        if self.frame_cache.get("is_on_interactable", None) is not None:
            return True

        blocks_hit = self.spritecollide(
            self.game_engine.current_level.entities,
            0, 0,
            trigger_cb=False,
            only_collideable=False
        )

        self.frame_cache["is_on_interactable"] = []
        for block in blocks_hit:
            if block.is_interactable():
                self.frame_cache["is_on_interactable"].append(block)

        if len(self.frame_cache["is_on_interactable"]) == 0:
            self.frame_cache["is_on_interactable"] = None
            return False

        return True

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
            elif event.key == self.controls.interact and self.is_on_code_block():
                # Stop the player and put them over the interactable object
                self.hard_stop()
                self.rect.left = self.frame_cache["is_on_code_block"].rect.left
                self.rect.bottom = self.frame_cache["is_on_code_block"].rect.bottom

                # Interact with the object
                self.frame_cache["is_on_code_block"].interact()
