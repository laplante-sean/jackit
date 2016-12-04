'''
Base class for all game actors. Computer or human controlled
'''

import pygame

class Actor(pygame.sprite.Sprite):
    '''
    Base class for all game actors
    '''

    def __init__(self, game_engine, sprite_width, sprite_height):
        super(Actor, self).__init__()

        # Store the game engine for access to globals
        self.game_engine = game_engine

        # Movement stats
        self.x_acceleration = 0.5       # Starting acceleration
        self.x_deceleration = 0.5       # Stopping acceleration
        self.top_speed = 6              # Fastest (in pixels) the actor moves
        self.jump_speed = 8            # Upward speed on jump
        self.air_braking = 0.15         # Ability to slow horizontal momentum while airborne
        self.grav_deceleration = 0.55   # Force of gravity while actor is ascending
        self.grav_acceleration = 1.05   # Force of gravity while actor is decending
        self.grav_high_jump = 0.25      # Force of gravity while actor is ascending and jump is held

        # Maximum number of frames it should take to stop movement
        self.max_stop_frames = int(self.top_speed/self.x_deceleration)

        # Number of frames the actor has been stopping for
        self.cur_stop_frame_count = 0

        # function to call to update movement based on current input
        self.horizontal_movement_action = self.stop

        # True if the actor is flying through the air like majesty
        self.jumping = False

        # Setup the sprite
        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([sprite_width, sprite_height])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        # Speed vector
        self.change_x = 0
        self.change_y = 0

    def update(self):
        '''
        Update actor position
        '''

        # Gravity
        self.calc_grav()

        # Update actor speed by executing the current movement action
        self.horizontal_movement_action()

        # Update the X direction
        self.rect.x += self.change_x

        # Check if we hit anything in the x direction
        blocks_hit = pygame.sprite.spritecollide(self, self.game_engine.platform_sprite_list, False)
        for block in blocks_hit:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        if len(blocks_hit):
            # Stop horizontal movement
            self.change_x = 0

        # Update te Y direction
        self.rect.y += self.change_y

        # Check if we hit anything in the y direction
        blocks_hit = pygame.sprite.spritecollide(self, self.game_engine.platform_sprite_list, False)
        for block in blocks_hit:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

        if len(blocks_hit):
            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        '''
        Calculate gravity
        '''

        # Are we on the ground? If so don't do gravity
        ground = self.game_engine.screen_height - self.rect.height
        if self.rect.y >= ground and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = ground
            return

        # Are we at the top of our arc? Switch to going down
        if self.change_y == 0:
            self.change_y = 1
        elif self.is_moving_up() and self.jumping: # are we holding jump? Jump higher
            self.change_y += self.grav_high_jump
        elif self.is_moving_up():
            self.change_y += self.grav_deceleration
        else:
            self.change_y += self.grav_acceleration

    def jump(self):
        '''
        Called when the user hits the jump button. Makes the character jump
        '''
        # If we're on the ground, it's OK to jump
        if self.rect.bottom >= self.game_engine.screen_height:
            self.change_y = (self.jump_speed * -1) # Up is negative
            self.jumping = True
        else:
            # Move down 2 pixels (doesn't work well with 1)
            self.rect.y += 2
            blocks_hit = pygame.sprite.spritecollide(
                self,
                self.game_engine.platform_sprite_list,
                False
            )
            self.rect.y -= 2 # Reset position after check

            if len(blocks_hit) > 0:
                self.change_y = (self.jump_speed * -1) # Up is negative
                self.jumping = True

    def go_left(self):
        '''
        Called when the user hits the left button. Moves the character left
        '''
        self.horizontal_movement_action = self.go_left

        if self.change_x <= (self.top_speed * -1):
            self.change_x = (self.top_speed * -1)
        elif self.is_moving_vertical() and self.is_moving_right():
            self.change_x += (self.air_braking * -1)
        else:
            self.change_x += (self.x_acceleration * -1)

    def go_right(self):
        '''
        Called when the user hits the right button. Moves the character right
        '''
        self.horizontal_movement_action = self.go_right

        if self.change_x >= self.top_speed:
            self.change_x = self.top_speed
        elif self.is_moving_left() and self.is_moving_vertical():
            self.change_x += self.air_braking
        else:
            self.change_x += self.x_acceleration

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
            self.change_x += (self.x_deceleration * -1)
        elif self.change_x < 0:
            self.change_x += self.x_deceleration
        else:
            self.change_x = 0

        self.cur_stop_frame_count += 1

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
