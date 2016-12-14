'''
User controllable player
'''

import pygame
from jackit.core import CustomEvent
from jackit.core.actor import Actor
from jackit.entities import CodeBlock, ExitBlock, DeathBlock, MoveableBlock

class Player(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine, controls, spawn_point=(0, 0)):
        super(Player, self).__init__(game_engine, 24, 24, spawn_point[0], spawn_point[1])
        self.controls = controls
        self.stats.use_patch = True # Use the UserPatch for player stats

    def collide(self, change_x, change_y, sprite):

        # If we're pushing a block don't collide with it
        '''
        if isinstance(sprite, MoveableBlock):
            keys = pygame.key.get_pressed()
            if keys[self.controls.push]:
                print("****Pushing/pulling block*****")
                return False # Overrides is_collidable() preventing collision with
                             # pushable blocks while pushing
        '''

        collideable = super(Player, self).collide(change_x, change_y, sprite)

        if isinstance(sprite, ExitBlock):
            print("Exit block")
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))
        elif isinstance(sprite, DeathBlock):
            print("Death block")
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":self}))

        return collideable

    def update(self):
        super(Player, self).update()

        # Move the pushable blocks with the player
        '''
        if self.is_pushable_on_left() or self.is_pushable_on_right():
            keys = pygame.key.get_pressed()
            if keys[self.controls.push]:
                left = self.frame_cache.get("is_pushabled_on_left", None)
                right = self.frame_cache.get("is_pushable_on_right", None)

                if left is not None:
                    left.rect.x = self.rect.x
                if right is not None:
                    right.rect.left = self.rect.x
        '''

    def is_pushable_on_right(self):
        '''
        True if there's a pushable block to the right of player
        '''
        if self.frame_cache.get("is_pushable_on_right", None) is not None:
            return True

        # See if there's a pushable block to the right of player
        self.rect.x += 2
        collideable_blocks_hit = self.spritecollide(
            self.game_engine.current_level.entities,
            0, 0,
            trigger_cb=False,
            only_collideable=True
        )
        self.rect.x -= 2

        if self.any_collideable:
            for block in collideable_blocks_hit:
                if isinstance(block, MoveableBlock):
                    # Only use the first b/c only one block should be able to be
                    # on our left or right at a time
                    self.frame_cache["is_pushable_on_right"] = block
                    return True

        return False

    def is_pushable_on_left(self):
        '''
        True if there's a pushable block to the left of player
        '''
        if self.frame_cache.get("is_pushable_on_left", None) is not None:
            return True

        # See if there's a pushable block to the left of player
        self.rect.x -= 2
        collideable_blocks_hit = self.spritecollide(
            self.game_engine.current_level.entities,
            0, 0,
            trigger_cb=False,
            only_collideable=True
        )
        self.rect.x += 2

        if self.any_collideable:
            for block in collideable_blocks_hit:
                if isinstance(block, MoveableBlock):
                    self.frame_cache["is_pushable_on_left"] = block
                    return True

        return False

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
