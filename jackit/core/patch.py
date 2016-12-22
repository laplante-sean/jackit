'''
The callbacks that the user can patch
'''

class PatchError(Exception):
    '''
    Something went wrong with the user's patch
    '''
    pass

class UserPatchSingleton:
    '''
    Class containing all the callbacks the user can patch
    '''
    _instance = None

    @classmethod
    def instance(cls):
        '''
        Get instance of EngineSingleton
        '''
        if cls._instance is None:
            cls._instance = UserPatchSingleton()
            return cls._instance
        return cls._instance

    def __init__(self):
        self.patch_map = {}

    def patch_method(self, method_name, cb, valid_ret_types, *args):
        '''
        Patch the method with the provided callback
        '''
        valid = False

        # Test the method and return value so we don't have to wrap it
        # in a try catch and test the return on each frame
        try:
            ret = cb(*args)
            for rtype in valid_ret_types:
                if isinstance(ret, rtype):
                    valid = True
                    break
            if not valid:
                raise PatchError("The return type from your patch is bad. Stop jerkin' around!")
        except BaseException as e:
            raise PatchError("Your code is bad and you should be sad about it: {}".format(e))

        if hasattr(self, method_name):
            self.patch_map[method_name] = cb
        else:
            raise PatchError("Trying to patch a method that doesn't exist'")

    def unpatch(self):
        '''
        Unpatch all the patched methods
        '''
        self.patch_map = {}

    def call_patch(self, method_name, *args):
        '''
        Call a patched method if it exists
        '''
        if self.patch_map.get(method_name, None) is not None:
            return self.patch_map[method_name](*args)
        return None

    def get_top_speed(self):
        '''
        Getter for the actors's top speed
        '''
        return self.call_patch(self.get_top_speed.__name__)

    def get_jump_speed(self):
        '''
        Getter for the actors's jump speed
        '''
        return self.call_patch(self.get_jump_speed.__name__)

    def get_x_acceleration(self):
        '''
        Getter for the actors's x-axis acceleration
        '''
        return self.call_patch(self.get_x_acceleration.__name__)

    def get_x_deceleration(self):
        '''
        Getter for the actos's x-axis deceleration
        '''
        return self.call_patch(self.get_x_deceleration.__name__)

    def get_grav_acceleration(self):
        '''
        Getter for the actor's gravity acceleration
        '''
        return self.call_patch(self.get_grav_acceleration.__name__)

    def get_grav_deceleration(self):
        '''
        Getter for the actor's gravity deceleration
        '''
        return self.call_patch(self.get_grav_deceleration.__name__)

    def get_grav_high_jump(self):
        '''
        Getter for the actor's gravity high jump value
        '''
        return self.call_patch(self.get_grav_high_jump.__name__)

    def is_moving_up(self, change_y):
        '''
        User patch getter to check if the sprite is moving up
        '''
        return self.call_patch(self.is_moving_up.__name__, change_y)

    def is_moving_down(self, change_y):
        '''
        User patch getter to check if the sprite is moving down
        '''
        return self.call_patch(self.is_moving_down.__name__, change_y)

    def get_terminal_velocity(self):
        '''
        User patch getter to get the player terminal velocity
        '''
        return self.call_patch(self.get_terminal_velocity.__name__)

# Create an instance of UserPatchSingleton
UserPatch = UserPatchSingleton.instance()
