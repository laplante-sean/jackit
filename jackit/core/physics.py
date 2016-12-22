'''
Basic physics for the game.
'''

from jackit.core.patch import UserPatch

class Physics:
    '''
    Basic physics for an object in the game. Not all values are used by all things
    that require physics. (e.g. not everything jumps)
    '''
    def __init__(self, x_acceleration=0.65, x_deceleration=0.9, top_speed=6,
                 jump_speed=8, air_braking=0.15, grav_acceleration=1.05,
                 grav_deceleration=0.55, grav_high_jump=0.25, terminal_velocity=20
                ):

        # Starting acceleration
        self._x_acceleration = x_acceleration

        # Stopping acceleration
        self._x_deceleration = x_deceleration

        # Fastest (in pixels) the actor moves
        self._top_speed = top_speed

        # Speed (in pixels) the actor leaves the ground
        self._jump_speed = jump_speed

        # Ability to slow horizontal momentum while airborne
        self.air_braking = air_braking

        # Force of gravity while actor is descending
        self._grav_acceleration = grav_acceleration

        # Force of gravity while actor is ascending
        self._grav_deceleration = grav_deceleration

        # Force of gravity while actor is ascending and jump is held
        self._grav_high_jump = grav_high_jump

        # Maximum falling speed
        self._terminal_velocity = terminal_velocity

        # True if patch methods should be used
        self.use_patch = False

    @property
    def terminal_velocity(self):
        '''
        Getter for _terminal_velocity - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._terminal_velocity

        ret = UserPatch.get_terminal_velocity()
        if ret is None:
            return self._terminal_velocity
        return ret

    @terminal_velocity.setter
    def terminal_velocity(self, value):
        self._terminal_velocity = value

    @property
    def grav_acceleration(self):
        '''
        Getter for _grav_acceleration - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._grav_acceleration

        ret = UserPatch.get_grav_acceleration()
        if ret is None:
            return self._grav_acceleration
        return ret

    @grav_acceleration.setter
    def grav_acceleration(self, value):
        self._grav_acceleration = value

    @property
    def grav_deceleration(self):
        '''
        Getter for _grav_deceleration - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._grav_deceleration

        ret = UserPatch.get_grav_deceleration()
        if ret is None:
            return self._grav_deceleration
        return ret

    @grav_deceleration.setter
    def grav_deceleration(self, value):
        self._grav_deceleration = value

    @property
    def grav_high_jump(self):
        '''
        Getter for _grav_high_jump - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._grav_high_jump

        ret = UserPatch.get_grav_high_jump()
        if ret is None:
            return self._grav_high_jump
        return ret

    @grav_high_jump.setter
    def grav_high_jump(self, value):
        self._grav_high_jump = value

    @property
    def x_acceleration(self):
        '''
        Getter for _x_acceleration - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._x_acceleration

        ret = UserPatch.get_x_acceleration()
        if ret is None:
            return self._x_acceleration
        return ret

    @x_acceleration.setter
    def x_acceleration(self, value):
        self._x_acceleration = value

    @property
    def x_deceleration(self):
        '''
        Getter for _x_deceleration - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._x_deceleration

        ret = UserPatch.get_x_deceleration()
        if ret is None:
            return self._x_deceleration
        return ret

    @x_deceleration.setter
    def x_deceleration(self, value):
        self._x_deceleration = value

    @property
    def top_speed(self):
        '''
        Getter for _top_speed - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._top_speed

        ret = UserPatch.get_top_speed()
        if ret is None:
            return self._top_speed
        return ret

    @top_speed.setter
    def top_speed(self, value):
        self._top_speed = value

    @property
    def jump_speed(self):
        '''
        Getter for _jump_speed - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._jump_speed

        ret = UserPatch.get_jump_speed()
        if ret is None:
            return self._jump_speed
        return ret

    @jump_speed.setter
    def jump_speed(self, value):
        self._jump_speed = value
