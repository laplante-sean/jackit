'''
Sprites for entities (platforms, items, code blocks, etc.)
'''

import pygame

from jackit.core import CustomEvent

class Entity(pygame.sprite.Sprite):
    '''
    Represents any entity that is not another player/enemy
    '''

    # TODO: Take an image/color argument to specify sprite image or color of block
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(Entity, self).__init__()

        # Store the game engine for access to globals
        self.game_engine = game_engine

        # Setup the sprite
        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 255, 0))
        self.image = self.image.convert() # Convert the image for faster blitting
        self.rect = self.image.get_rect()

        # Initial position
        self.rect.x = x_pos
        self.rect.y = y_pos

        # True if the player should be able to interact with this block by hitting a button
        self.interactable = False

        # True if the player should collide with this entity
        self.collideable = True

        # True if an entity is moveable
        self.moveable = False

    def update(self):
        '''
        Check if an entity is in the death zone and trigger an event to remove it
        '''
        if self.game_engine.is_rect_in_death_zone(self.rect):
            pygame.event.post(pygame.event.Event(CustomEvent.DESPAWN_ENTITY, {"entity": self}))

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

    def is_moveable(self):
        '''
        Getter for the moveable instance variable
        '''
        return self.moveable

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

    def collide(self, _actor):
        '''
        Called when an actor collides with this entity
        '''
        return
