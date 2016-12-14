'''
Base class for jackit sprite
'''

import pygame

from jackit.core import CustomEvent
from jackit.core.physics import Physics

class Sprite(pygame.sprite.Sprite):
    '''
    Derives from pygame spriten for update and draw
    and so it can be included in sprite groups
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, stats=Physics()):
        super(Sprite, self).__init__()

        # Store the game engine for access to globals
        self.game_engine = game_engine

        # Store the width and height
        self.width = width
        self.height = height

        # Store the stats
        self.stats = stats

        # Setup the sprite
        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 0, 0))
        self.image = self.image.convert() # Convert the surface for faster blitting
        self.rect = self.image.get_rect()

        # Store the initial spawn point for this sprite forever
        self.spawn_point = (x_pos, y_pos)

        self.rect.x = x_pos
        self.rect.y = y_pos

        # Speed vector if the sprite moves
        self.change_x = 0
        self.change_y = 0

        # True if the player should be able to interact with this block by hitting a button
        self.interactable = False

        # True if the player should collide with this entity
        self.collideable = True

        # True if any of the sprites from the most recent call to spritecollide() were collideable
        self.any_collideable = False

        # True if this sprite kills the player
        self.kills_player = False

        # Frame cache. Allows methods that do a lot to store their results
        # for the current frame so that subsequent calls use the cache. This
        # is cleared on each frame.
        self.frame_cache = {}

    def update(self):
        '''
        Update the sprite's position.
        '''

        # Don't waist time if we're not moving
        if self.change_x == 0 and self.change_y == 0:
            # Clear the frame cache here as well
            # this is in case someone overrides update
            # and calls a method that uses the frame cache
            self.frame_cache.clear()
            return

        # Update the X direction
        self.rect.x += self.change_x

        # Check if we hit anything in the x direction and stop moving if we did
        self.spritecollide(self.game_engine.current_level.entities, self.change_x, 0)
        if self.any_collideable:
            self.change_x = 0

        # Update the Y direction
        self.rect.y += self.change_y

        # Check if we hit anything in the y direction and stop moving if we did
        self.spritecollide(self.game_engine.current_level.entities, 0, self.change_y)
        if self.any_collideable:
            self.change_y = 0

        # Check if we're in the death zone of the level and kill ourself
        if self.game_engine.is_rect_in_death_zone(self.rect):
            print("Death zone: (", self.rect.x, ",", self.rect.y, ")")
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite": self}))

        # Clear the frame cache
        self.frame_cache.clear()

    def spritecollide(self, sprites, change_x, change_y, trigger_cb=True, only_collideable=False):
        '''
        Checks if this sprite collides with any sprite in
        the level ignoring itself
        @param trigger_cb - True if self.collide() should be called
        @param only_collideable - True if return should only contains sprites that
                                  are collideable
        '''
        collided_with = []
        self.any_collideable = False
        for sprite in sprites:
            if sprite is self:
                continue

            if pygame.sprite.collide_rect(self, sprite):
                if not only_collideable:
                    collided_with.append(sprite)
                elif sprite.is_collideable():
                    collided_with.append(sprite)

                if trigger_cb:
                    collideable = self.collide(change_x, change_y, sprite)
                    if collideable:
                        self.any_collideable = True
                elif sprite.is_collideable():
                    self.any_collideable = True

        return collided_with

    def collide(self, change_x, change_y, sprite):
        '''
        Handle collisions
        '''

        # Called on the sprite being collided with
        sprite.collide_with(self)

        if sprite.is_collideable():
            if change_x > 0:
                self.rect.right = sprite.rect.left
            if change_x < 0:
                self.rect.left = sprite.rect.right
            if change_y > 0:
                self.rect.bottom = sprite.rect.top
            if change_y < 0:
                self.rect.top = sprite.rect.bottom
            return True
        return False

    def is_on_collideable(self):
        '''
        True if Sprite is on a collideable entity
        uses frame cache to ensure subsequent calls
        are faster
        '''

        # Speed up calls to this method if used more than once per frame
        if self.frame_cache.get("is_on_collideable", None) != None:
            return True

        # Move down 2 pixels (doesn't work well with 1)
        self.rect.y += 2
        collideable_blocks_hit = self.spritecollide(
            self.game_engine.current_level.entities,
            0, 0,
            trigger_cb=False,
            only_collideable=True
        )
        self.rect.y -= 2 # Reset position after check

        if self.any_collideable:
            self.frame_cache["is_on_collideable"] = collideable_blocks_hit
            return True

        return False

    def reset(self):
        '''
        Reset the sprite to its starting position
        Also stops movement
        '''
        self.rect.x = self.spawn_point[0]
        self.rect.y = self.spawn_point[1]
        self.hard_stop()

    def is_interactable(self):
        '''
        Getter for the interactable instance variable
        '''
        return self.interactable

    def is_collideable(self):
        '''
        Getter for the collideable instance variable
        '''
        return self.collideable

    def interact(self):
        '''
        Called when an interactable block is interacted with
        '''
        return

    def interaction_complete(self, _event):
        '''
        Called when an interaction is complete with an interactable block
        '''
        return

    def collide_with(self, _sprite):
        '''
        Called on the sprite being collided with
        '''
        return

    def hard_stop(self):
        '''
        Stop the player immediately
        '''
        self.change_x = 0
        self.change_y = 0

    def is_moving_left(self):
        '''
        True if the Actor is moving left
        '''
        return self.change_x < 0

    def is_moving_right(self):
        '''
        True if the Actor is moving right
        '''
        return self.change_x > 0

    def is_moving_up(self):
        '''
        True if the Actor is moving up
        '''
        return self.change_y < 0

    def is_moving_down(self):
        '''
        True if the Actor is moving down
        '''
        return self.change_y > 0

    def is_moving_horizontal(self):
        '''
        True if the Actor is moving on the X-axis
        '''
        return abs(self.change_x) > 0

    def is_moving_vertical(self):
        '''
        True if the Actor is moving on the Y-axis
        '''
        return abs(self.change_y) > 0

    def is_moving(self):
        '''
        True if the Actor is moving
        '''
        return self.change_x != 0 or self.change_y != 0
