'''
Base class for all game actors. Computer or human controlled
'''

from jackit.core.sprite import Sprite
from jackit.core.physics import Physics

class Actor(Sprite):
    '''
    Base class for all game actors
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos, stats=Physics()):
        super(Actor, self).__init__(game_engine, width, height, x_pos, y_pos, stats)

        # Maximum number of frames it should take to stop movement
        self.max_stop_frames = int(self.stats.top_speed/self.stats.x_deceleration)

        # Number of frames the actor has been stopping for
        self.cur_stop_frame_count = 0

        # function to call to update movement based on current input
        self.horizontal_movement_action = self.stop

        # True if the actor is flying through the air like majesty
        self.jumping = False

    def update(self):
        '''
        Update actor position
        '''

        # Gravity
        self.calc_grav()

        # Update actor speed by executing the current movement action
        self.horizontal_movement_action()

        # Call the base class update
        super(Actor, self).update()

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
