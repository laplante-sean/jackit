'''
User controllable player
'''

import os
import pygame
from deploy import SiteDeployment
from jackit.core.animation import SpriteStripAnimation
from jackit.core import CustomEvent
from jackit.core.actor import Actor
from jackit.actors.enemy import Enemy
from jackit.entities import CodeBlock, ExitBlock, DeathBlock,\
                            DecryptionKey, Coin, OneUp

class Player(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine, controls, spawn_point=(0, 0)):
        block_width = game_engine.current_level.level_map_block_x
        block_height = game_engine.current_level.level_map_block_y
        image_path = os.path.join(SiteDeployment.resource_path, "sprites", "animation_demo.bmp")

        animation = SpriteStripAnimation(
            image_path, (0, 0, block_width, block_height), 8, -1, True,
            int(game_engine.config.framerate / 24)
        ) + SpriteStripAnimation(
            image_path, (0, 24, block_width, block_height), 8, -1, True,
            int(game_engine.config.framerate / 24)
        ) + SpriteStripAnimation(
            image_path, (0, 48, block_width, block_height), 8, -1, True,
            int(game_engine.config.framerate / 24)
        ) + SpriteStripAnimation(
            image_path, (0, 72, block_width, block_height), 8, -1, True,
            int(game_engine.config.framerate / 24)
        )

        super(Player, self).__init__(
            game_engine, block_width, block_height, spawn_point[0],
            spawn_point[1], animation=animation
        )

        self.controls = controls
        self.use_patch = True # Use the UserPatch for player stats and player

        # Current level score
        self.level_score = 0

        # List of items the player has
        self.items = []

        # List of stored code routines (so they don't have to do the code blocks_hit
        # every time)
        self.stored_code = []

        # True if the player is alive otherwise false
        self.alive = True

    def has_key(self):
        '''
        Does the player have the decryption key?
        '''
        return any(isinstance(x, DecryptionKey) for x in self.items)

    def collide(self, change_x, change_y, sprite):
        '''
        Called on each collision
        '''
        collideable = super(Player, self).collide(change_x, change_y, sprite)

        if isinstance(sprite, Coin):
            self.level_score += sprite.points
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":sprite}))
        elif isinstance(sprite, OneUp):
            self.game_engine.lives += 1
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":sprite}))
        elif isinstance(sprite, DecryptionKey):
            print("Got decryption key")
            self.items.append(sprite)
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":sprite}))
        elif isinstance(sprite, ExitBlock):
            print("Exit block")
            self.game_engine.total_score += self.level_score
            self.items.clear()
            self.level_score = 0
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))
        elif isinstance(sprite, Enemy) or isinstance(sprite, DeathBlock):
            print("collide() kills player. Player collided with enemy or death block.")
            self.kill()

        return collideable

    def reset(self):
        '''
        Reset the player
        '''
        super(Player, self).reset()
        self.alive = True

    def kill(self):
        '''
        Kill the player
        '''
        if not self.alive:
            return

        self.game_engine.lives -= 1
        if self.game_engine.lives <= 0:
            self.game_engine.running = False

        self.items.clear()
        self.level_score = 0

        self.alive = False
        pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":self}))

    def is_on_collideable(self):
        '''
        The rare chance that we land perfectly on an enemy and miss the call to collide
        '''
        ret = super(Player, self).is_on_collideable()
        if ret:
            for block in self.frame_cache["is_on_collideable"]:
                if isinstance(block, Enemy):
                    print("*******Somehow missed this one. On enemy!")
                    pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite":self}))
                    break
        return ret

    def collide_with(self, sprite):
        '''
        Some other sprite collided into us (we didn't collide into it)
        Happens when the other sprite is moving and this sprite is not
        '''
        if isinstance(sprite, Enemy):
            print("collide_with() kills player. Enemy or death block collided with player.")
            self.kill()

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
                if self.frame_cache["is_on_code_block"].is_locked() and not self.has_key():
                    print("This block is encrypted. Needs key!")
                    return

                # Stop the player and put them over the interactable object
                self.hard_stop()
                self.rect.left = self.frame_cache["is_on_code_block"].rect.left
                self.rect.bottom = self.frame_cache["is_on_code_block"].rect.bottom

                # Interact with the object
                self.frame_cache["is_on_code_block"].interact()
