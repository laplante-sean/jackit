'''
Base class for all game actors. Computer or human controlled
'''

import pygame

from jackit.core import CustomEvent

class ActorStats:
    '''
    Stats for an actor
    '''
    def __init__(self, x_acceleration=0.5, x_deceleration=0.5, top_speed=6,
                 jump_speed=8, air_braking=0.15, grav_acceleration=1.05,
                 grav_deceleration=0.55, grav_high_jump=0.25, terminal_velocity=20
                ):

        # Starting acceleration
        self.x_acceleration = x_acceleration

        # Stopping acceleration
        self.x_deceleration = x_deceleration

        # Fastest (in pixels) the actor moves
        self.top_speed = top_speed

        # Speed (in pixels) the actor leaves the ground
        self.jump_speed = jump_speed

        # Ability to slow horizontal momentum while airborne
        self.air_braking = air_braking

        # Force of gravity while actor is descending
        self.grav_acceleration = grav_acceleration

        # Force of gravity while actor is ascending
        self.grav_deceleration = grav_deceleration

        # Force of gravity while actor is ascending and jump is held
        self.grav_high_jump = grav_high_jump

        # Maximum falling speed
        self.terminal_velocity = terminal_velocity

class Actor(pygame.sprite.Sprite):
    '''
    Base class for all game actors
    '''
    def __init__(self, game_engine, sprite_width, sprite_height, actor_stats=ActorStats()):
        super(Actor, self).__init__()

        # Store the game engine for access to globals
        self.game_engine = game_engine

        # Setup the actor stats
        self.stats = actor_stats

        # Maximum number of frames it should take to stop movement
        self.max_stop_frames = int(self.stats.top_speed/self.stats.x_deceleration)

        # Number of frames the actor has been stopping for
        self.cur_stop_frame_count = 0

        # function to call to update movement based on current input
        self.horizontal_movement_action = self.stop

        # True if the actor is flying through the air like majesty
        self.jumping = False

        # Entity() object if the Actor is colliding with an interactable block otherwise None
        self.on_interactable_block = None

        # Setup the sprite
        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([sprite_width, sprite_height])
        self.image.fill((255, 0, 0))
        self.image = self.image.convert() # Convert the surface for faster blitting
        self.rect = self.image.get_rect()

        # Speed vector
        self.change_x = 0
        self.change_y = 0

        # Frame cache. Allows methods that do a lot on each call to store results
        # for the current frame Useful for things that check for collisions
        # like is_on_collideable()
        self.frame_cache = {}

    def update(self):
        '''
        Update actor position
        '''

        # Reset each frame
        self.on_interactable_block = None

        # Gravity
        self.calc_grav()

        # Update actor speed by executing the current movement action
        self.horizontal_movement_action()

        # Update the X direction
        self.rect.x += self.change_x

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
            pygame.event.post(pygame.event.Event(CustomEvent.KILL_ACTOR, {"actor": self}))

        # Clear the frame cache
        self.frame_cache.clear()

    def collide(self, change_x, change_y, entity):
        '''
        Handle collisions
        '''

        # Call the entity's collide method to handle
        # things like ExitBlock triggering an exit
        entity.collide(self)

        if entity.is_collideable():
            if change_x > 0:
                self.rect.right = entity.rect.left
            if change_x < 0:
                self.rect.left = entity.rect.right
            if change_y > 0:
                self.rect.bottom = entity.rect.top
            if change_y < 0:
                self.rect.top = entity.rect.bottom

    def calc_grav(self):
        '''
        Calculate gravity
        '''
        if self.is_on_collideable() and self.change_y >= 0:
            self.change_y = 0
            return

        if self.change_y == 0:
            # Are we at the top of our arc? Switch to going down
            self.change_y = 1
        elif self.is_moving_up() and self.jumping:
            # are we holding jump? Jump higher
            self.change_y += self.stats.grav_high_jump
        elif self.is_moving_up():
            # Jump normal
            self.change_y += self.stats.grav_deceleration
        elif self.change_y >= self.stats.terminal_velocity:
            # Don't fall too fast
            self.change_y = self.stats.terminal_velocity
        else:
            # Fall normal
            self.change_y += self.stats.grav_acceleration

    def jump(self):
        '''
        Called when the user hits the jump button. Makes the character jump
        '''
        if self.is_on_collideable():
            self.change_y = (self.stats.jump_speed * -1) # Up is negative
            self.jumping = True

    def go_left(self):
        '''
        Called when the user hits the left button. Moves the character left
        '''
        self.horizontal_movement_action = self.go_left

        if self.change_x <= (self.stats.top_speed * -1):
            self.change_x = (self.stats.top_speed * -1)
        elif (not self.is_on_collideable()) and self.is_moving_right():
            self.change_x += (self.stats.air_braking * -1)
        else:
            self.change_x += (self.stats.x_acceleration * -1)

    def go_right(self):
        '''
        Called when the user hits the right button. Moves the character right
        '''
        self.horizontal_movement_action = self.go_right

        if self.change_x >= self.stats.top_speed:
            self.change_x = self.stats.top_speed
        elif self.is_moving_left() and (not self.is_on_collideable()):
            self.change_x += self.stats.air_braking
        else:
            self.change_x += self.stats.x_acceleration

    def stop_jumping(self):
        '''
        Called when the jump key is released
        '''
        self.jumping = False

    def stop(self):
        '''
        Stops the characters movement when the user releases the keys
        '''
        self.horizontal_movement_action = self.stop

        # Don't allow sopping while in the air
        if self.is_moving_vertical():
            return

        # Don't allow this to take longer than it should. Avoids getting stuck
        # never reaching 0 if x_deceleration isn't evenly divisible by top_speed
        if self.cur_stop_frame_count >= self.max_stop_frames or self.change_x == 0:
            self.change_x = 0
            self.cur_stop_frame_count = 0
            return

        if self.change_x > 0:
            self.change_x += (self.stats.x_deceleration * -1)
        elif self.change_x < 0:
            self.change_x += self.stats.x_deceleration
        else:
            self.change_x = 0

        self.cur_stop_frame_count += 1

    def hard_stop(self):
        '''
        Stop the player immediately
        '''
        self.change_x = 0
        self.change_y = 0

    def is_on_collideable(self):
        '''
        True if Actor is on a platform
        '''

        # Speed up calls to this method if used more than once per frame
        if self.frame_cache.get("is_on_collideable", None) != None:
            return len(self.frame_cache["is_on_collideable"]) > 0

        # Move down 2 pixels (doesn't work well with 1)
        self.rect.y += 2
        blocks_hit = pygame.sprite.spritecollide(
            self,
            self.game_engine.current_level.entities,
            False
        )
        self.rect.y -= 2 # Reset position after check

        # Update the frame cache with platforms we're on
        self.frame_cache["is_on_collideable"] = blocks_hit

        if any(x.is_collideable() for x in blocks_hit):
            return True

        return False

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
