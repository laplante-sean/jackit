'''
Basic physics for the game.
'''

from jackit.core.patch import UserPatch

class Physics:
    '''
    Basic physics for an object in the game. Not all values are used by all things
    that require physics. (e.g. not everything jumps)
    '''
    def __init__(self, x_acceleration=0.5, x_deceleration=0.8, top_speed=6,
                 jump_speed=8, air_braking=0.15, grav_acceleration=1.05,
                 grav_deceleration=0.55, grav_high_jump=0.25, terminal_velocity=20,
                 weighted_acceleration=0.05, weighted_top_speed=4
                ):

        # Starting acceleration
        self._x_acceleration = x_acceleration

        # Stopping acceleration
        self.x_deceleration = x_deceleration

        # Fastest (in pixels) the actor moves
        self._top_speed = top_speed

        # Speed (in pixels) the actor leaves the ground
        self._jump_speed = jump_speed

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

        # Acceleration when pushing an object
        self._weighted_acceleration = weighted_acceleration

        # Top speed when pushing an object
        self._weighted_top_speed = weighted_top_speed

        # True if the weighted values for speed and acceleration should be used instead
        self.pushing = False

        # True if patch methods should be used
        self.use_patch = False

    @property
    def x_acceleration(self):
        '''
        Getter for x_acceleration - Calls the patched version if it exists
        '''
        if not self.use_patch:
            if self.pushing:
                return self._weighted_acceleration
            return self._x_acceleration

        ret = UserPatch.get_actor_x_acceleration()
        if ret is None:
            return self._x_acceleration
        return ret

    @property
    def top_speed(self):
        '''
        Getter for top_speed - Calls the patched version if it exists
        '''
        if not self.use_patch:
            if self.pushing:
                return self._weighted_top_speed
            return self._top_speed

        ret = UserPatch.get_actor_top_speed()
        if ret is None:
            return self._top_speed
        return ret

    @property
    def jump_speed(self):
        '''
        Getter for jump_speed - Calls the patched version if it exists
        '''
        if not self.use_patch:
            return self._jump_speed

        ret = UserPatch.get_actor_jump_speed()
        if ret is None:
            return self._jump_speed
        return ret
