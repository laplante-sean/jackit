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

    def patch_method(self, method_name, cb):
        '''
        Patch the method with the provided callback
        '''
        print("Patching method:", method_name, "with", cb)

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
        try:
            if self.patch_map.get(method_name, None) is not None:
                return self.patch_map[method_name]()
        except BaseException:
            raise PatchError("This patch  for {}, was no good!".format(method_name))
        return None

    def validate_float(self, value):
        '''
        Validate an float value
        '''
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                raise PatchError("Invalid float: {}".format(value))
        elif isinstance(value, float) or isinstance(value, int):
            return value
        else:
            raise PatchError("Invalid. Return is not a float: {}".format(type(value)))

    def get_actor_top_speed(self):
        '''
        Getter for the player's top speed
        '''
        ret = self.call_patch(self.get_actor_top_speed.__name__)
        if ret is not None:
            return self.validate_float(ret)
        return None

    def get_actor_jump_speed(self):
        '''
        Getter for the player's jump speed
        '''
        ret = self.call_patch(self.get_actor_jump_speed.__name__)
        if ret is not None:
            return self.validate_float(ret)
        return None

    def get_actor_x_acceleration(self):
        '''
        Getter for the player's x-axis acceleration
        '''
        ret = self.call_patch(self.get_actor_x_acceleration.__name__)
        if ret is not None:
            return self.validate_float(ret)
        return None

# Create an instance of UserPatchSingleton
UserPatch = UserPatchSingleton.instance()
