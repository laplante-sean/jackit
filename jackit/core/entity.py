'''
Sprites for entities (platforms, items, code blocks, etc.)
'''

import pygame

from jackit.core import CustomEvent
from jackit.core.player import Player

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

class PlatformStats:
    '''
    Stats for a moving platform
    '''
    def __init__(self, change_x=0, change_y=0, x_travel_dist=0, y_travel_dist=0, acceleration=0):
        self.change_x = change_x
        self.change_y = change_y
        self.x_travel_dist = x_travel_dist
        self.y_travel_dist = y_travel_dist
        self.acceleration = acceleration

class Platform(Entity):
    '''
    Represents a platform that actors can stand on
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, platform_stats=PlatformStats()):
        super(Platform, self).__init__(game_engine, width, height, x_pos, y_pos)

        # Movement stats if it's moving platform
        self.stats = platform_stats

        # Distance it's traveled since last turn around
        self.cur_x_travel_dist = 0
        self.cur_y_travel_dist = 0

        # Current speed vector
        self.change_x = self.stats.change_x
        self.change_y = self.stats.change_y

    def update(self):
        '''
        Update platform position
        '''
        self.cur_x_travel_dist += abs(self.change_x)
        self.cur_y_travel_dist += abs(self.change_y)

        if self.cur_x_travel_dist >= self.stats.x_travel_dist:
            self.stats.change_x *= -1
            self.change_x = self.stats.change_x
            self.cur_x_travel_dist = 0

        if self.cur_y_travel_dist >= self.stats.y_travel_dist:
            self.stats.change_y *= -1
            self.change_y = self.stats.change_y
            self.cur_y_travel_dist = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y

class ExitBlock(Entity):
    '''
    Exit block. Moves to the next level
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(ExitBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((255, 0, 0))

    def collide(self, actor):
        if isinstance(actor, Player):
            pygame.event.post(pygame.event.Event(CustomEvent.NEXT_LEVEL))

class CodeBlock(Entity):
    '''
    Code block. Used to bring up the code view
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(CodeBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((254, 68, 123))
        self.interactable = True
        self.collideable = False
        self.interaction_guard = pygame.sprite.Group()
        self.challenge_text = "CHALLENGE TEXT"

    def collide(self, actor):
        actor.on_interactable_block = self

    def interact(self):
        '''
        Called when an interactable block is interacted with
        '''

        # Guard rects to the left, right, and above the interactable object
        self.interaction_guard.add(
            self.game_engine.current_level.create_platform(
                (self.rect.left - self.game_engine.current_level.level_map_block_x),
                (self.rect.top)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.left - self.game_engine.current_level.level_map_block_x),
                (self.rect.top - self.game_engine.current_level.level_map_block_y)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.right),
                (self.rect.top)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.right),
                (self.rect.top - self.game_engine.current_level.level_map_block_y)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.left),
                (self.rect.top - self.game_engine.current_level.level_map_block_y)
            )
        )

        self.game_engine.current_level.entities.add(self.interaction_guard)

        # Start doing the code
        self.game_engine.code_editor.run(self.challenge_text)

    def interaction_complete(self, event):
        '''
        Called when the interaction is complete
        '''

        print("Code: ", event.text)

        try:
            # pylint: disable=W0122
            exec(event.text)
        except BaseException as e:
            print("Your code blows! ", str(e))

        # Remove the interaction guard from around the object
        self.game_engine.current_level.entities.remove(self.interaction_guard)

        # TODO: Create a sprite.Group of sprites to clear from the screen.
        # Make it part of the Level base class. In Level update, clear the list
        self.interaction_guard.clear(self.game_engine.screen, (0, 0, 255))

