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

    def patch_method(self, method_name, cb, valid_ret_types):
        '''
        Patch the method with the provided callback
        '''
        valid = False

        # Test the method and return value so we don't have to wrap it
        # in a try catch and test the return on each frame
        try:
            ret = cb()
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

    def call_patch(self, method_name):
        '''
        Call a patched method if it exists
        '''
        if self.patch_map.get(method_name, None) is not None:
            return self.patch_map[method_name]()
        return None

    def get_actor_top_speed(self):
        '''
        Getter for the player's top speed
        '''
        return self.call_patch(self.get_actor_top_speed.__name__)

    def get_actor_jump_speed(self):
        '''
        Getter for the player's jump speed
        '''
        return self.call_patch(self.get_actor_jump_speed.__name__)

    def get_actor_x_acceleration(self):
        '''
        Getter for the player's x-axis acceleration
        '''
        return self.call_patch(self.get_actor_x_acceleration.__name__)

# Create an instance of UserPatchSingleton
UserPatch = UserPatchSingleton.instance()
