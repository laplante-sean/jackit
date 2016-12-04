'''
Base class for all game actors. Computer and human controlled
'''

from jackit.core import EngineComponent
from jackit.core.sprite import Sprite

class Actor(EngineComponent):
    '''
    Base class for all game actors
    '''

    def __init__(self, game_engine):
        super(Actor, self).__init__(game_engine)
        # Movement stats
        self.x_acceleration = 0.5       # Starting acceleration
        self.x_deceleration = 0.5       # Stopping acceleration
        self.top_speed = 6              # Fastest (in pixels) the actor moves
        self.jump_speed = 10            # Upward speed on jump
        self.air_braking = 0.15         # Ability to slow horizontal momentum while airborne
        self.grav_acceleration = 0.35   # Force of gravity

        # Maximum number of frames it should take to stop movement
        self.max_stop_frames = int(self.top_speed/self.x_deceleration)

        # Number of frames the actor has been stopping for
        self.cur_stop_frame_count = 0

        # Create the sprite and add it to the game engine
        self.sprite = Sprite((255, 0, 0), 25, 50)
        self.game_engine.active_sprite_list.add(self.sprite)

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # function to call to update movement based on current input
        self.horizontal_movement_action = self.stop

    def update(self):
        '''
        Update actor position
        '''

        # Gravity
        self.calc_grav()

        # Update actor speed by executing the current movement action
        self.horizontal_movement_action()

        # Move left/right
        self.sprite.prep_change_x(self.change_x)

        '''
        # See if we hit anything in the x direction
        block_hit_list = self.sprite.get_collide_blocks(self.game_engine.active_sprite_list)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.sprite.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.sprite.rect.left = block.rect.right
        '''

        # Move up/down
        self.sprite.prep_change_y(self.change_y)

        '''
        # Check and see if we hit anything
        block_hit_list = self.sprite.get_collide_blocks(self.game_engine.active_sprite_list)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.sprite.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.sprite.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0
        '''

        # Commit the change after all the collision detection and whatnot
        self.sprite.commit_change()

    def calc_grav(self):
        '''
        Calculate gravity
        '''
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += self.grav_acceleration

        # See if we are on the ground.
        # TODO: Check if the change_y will put us through the ground and adjust
        ground = self.game_engine.screen_height - self.sprite.rect.height
        if self.sprite.rect.y >= ground and self.change_y >= 0:
            self.change_y = 0
            self.sprite.rect.y = ground

    def jump(self):
        '''
        Called when the user hits the jump button. Makes the character jump
        '''

        # If we're on the ground, it's OK to jump
        if self.sprite.rect.bottom >= self.game_engine.screen_height:
            self.change_y = (self.jump_speed * -1) # Up is negative
        else:
            # TODO: Check if we're on a platform
            # Move down 2 pixels (doesn't work well with 1)
            self.sprite.rect.y += 2
            platform_hit_list = self.sprite.get_collide_blocks([])
            self.sprite.rect.y -= 2 # Reset position after check

            if len(platform_hit_list) > 0:
                self.change_y = (self.jump_speed * -1) # Up is negative

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
