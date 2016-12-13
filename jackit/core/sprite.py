'''
Base class for jackit sprite
'''

import pygame

from jackit.core import CustomEvent

class Sprite(pygame.sprite.Sprite):
    '''
    Derives from pygame spriten for update and draw
    and so it can be included in sprite groups
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Sprite, self).__init__()

        # Store the game engine for access to globals
        self.game_engine = game_engine

        self.width = width
        self.height = height

        # Setup the sprite
        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 0, 0))
        self.image = self.image.convert() # Convert the surface for faster blitting
        self.rect = self.image.get_rect()

        self.rect.x = x_pos
        self.rect.y = y_pos

        # Speed vector if the sprite moves
        self.change_x = 0
        self.change_y = 0

        # True if the player should be able to interact with this block by hitting a button
        self.interactable = False

        # True if the player should collide with this entity
        self.collideable = True

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
            self.frame_cache.clear()
            return

        # Update the X direction
        self.rect.x += self.change_x

        # TODO: handle collisions with all things, entities and actors
        # Except for self. (Create a list of all things but remove self)

        # Check if we hit anything in the x direction and stop moving if we did
        blocks_hit = pygame.sprite.spritecollide(
            self, self.game_engine.current_level.entities, False)
        for block in blocks_hit:
            self.collide(self.change_x, 0, block)
        if any(x.is_collideable() for x in blocks_hit):
            self.change_x = 0

        # Update the Y direction
        self.rect.y += self.change_y

        # Check if we hit anything in the y direction and stop moving if we did
        blocks_hit = pygame.sprite.spritecollide(
            self, self.game_engine.current_level.entities, False)
        for block in blocks_hit:
            self.collide(0, self.change_y, block)
        if any(x.is_collideable() for x in blocks_hit):
            self.change_y = 0

        # Check if we're in the death zone of the level and kill ourself
        if self.game_engine.is_rect_in_death_zone(self.rect):
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_SPRITE, {"sprite": self}))

        # Clear the frame cache
        self.frame_cache.clear()

    def collide(self, change_x, change_y, sprite):
        '''
        Handle collisions
        '''

        # Call the objects collide_with method to handle
        # things like ExitBlock triggering an exit
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

    def collide_with(self, _sprite):
        '''
        Called when a sprite has collided with this sprite.
        Override to handle things like death blocks and exit blocks
        '''
        return

    def is_on_collideable_entity(self):
        '''
        True if Sprite is on a collideable entity
        uses frame cache to ensure subsequent calls
        are faster
        '''

        # Speed up calls to this method if used more than once per frame
        if self.frame_cache.get("is_on_collideable_entity", None) != None:
            return len(self.frame_cache["is_on_collideable_entity"]) > 0

        # Move down 2 pixels (doesn't work well with 1)
        self.rect.y += 2
        blocks_hit = pygame.sprite.spritecollide(
            self,
            self.game_engine.current_level.entities,
            False
        )
        self.rect.y -= 2 # Reset position after check

        # Update the frame cache with platforms we're on
        self.frame_cache["is_on_collideable_entity"] = blocks_hit

        if any(x.is_collideable() for x in blocks_hit):
            return True

        return False

    def is_on_collideable_actor(self):
        '''
        True if Sprite is on a collideable actor
        uses frame cache to ensure subsequent calls
        are faster
        '''

        # Speed up calls to this method if used more than once per frame
        if self.frame_cache.get("is_on_collideable_actor", None) != None:
            return len(self.frame_cache["is_on_collideable_actor"]) > 0

        # TODO: make a method to get actors that aren't self
        # so that we can include player in the actor list
        # and so that entities can collide with other entities
        # in the method above

        # Move down 2 pixels (doesn't work well with 1)
        self.rect.y += 2
        blocks_hit = pygame.sprite.spritecollide(
            self,
            self.game_engine.current_level.actors,
            False
        )
        self.rect.y -= 2 # Reset position after check

        # Update the frame cache with platforms we're on
        self.frame_cache["is_on_collideable_actor"] = blocks_hit

        if any(x.is_collideable() for x in blocks_hit):
            return True

        return False

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
