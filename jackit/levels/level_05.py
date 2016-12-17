'''
Fifth level
'''

from jackit.core.level import Level
from jackit.core.patch import UserPatch

class Level_05(Level):
    '''
    Fifth level - Reverse gravity like a boss
    '''

    _map = [
        "                                      PPPPPPPPPPPPDD             ",
        "                                      P            D             ",
        "                                      P            D             ",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP  D         PPPPPPPPPPPPPP",
        "P            I   I   I   I   I           D I  I  I D           EP",
        "P                                        DPPPPPPPPPD           EP",
        "PS C                                     DDDDDDDDDDD       PPPPPP",
        "PPPPPP                                                          ",
        "                                    I   I   I                   ",
        "                                 PPPPPPPPPPPPPPP                ",
        "                                    I   I   I            I      ",
        "                                                   PPPPPPPPPP   ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                                                ",
        "                                       IIIIIIIIIII              ",
        "                                       PPPPPPPPPPP              "
    ]

    _challenges = [
        """# There's items up there!
def get_actor_grav_acceleration():
    # Get the force of gravity when the player is falling
    return 0

def get_actor_grav_deceleration():
    # Get the force of gravity when the player is going up
    return 0

def get_actor_grav_high_jump():
    # Get the reduced force of gravity while jump is held
    return 0

def is_moving_up(change_y):
    return change_y < 0
        """
    ]

    def __init__(self, game_engine):
        super(Level_05, self).__init__(game_engine, Level_05._map)
        self.num_code_blocks_created = 0

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_05, self).create_code_block(x_pos, y_pos)

        block.challenge_text = Level_05._challenges[self.num_code_blocks_created]
        self.num_code_blocks_created += 1

        return block

    def unload(self):
        super(Level_05, self).unload()
        self.num_code_blocks_created = 0

    def challenge_completed(self, code_obj):
        '''
        Called when a code block is exited after
        the entered code is validated and compiled
        '''
        local_dict = locals()

        # Execute the code object
        try:
            # pylint: disable=W0122
            exec(code_obj, globals(), local_dict)
        except BaseException as e:
            print("That's some bad code! ", str(e))

        # Patch the provided methods
        if local_dict.get("get_actor_grav_acceleration", None) is not None:
            UserPatch.patch_method("get_actor_grav_acceleration",
                                   local_dict.get("get_actor_grav_acceleration"),
                                   [float, int])
        if local_dict.get("get_actor_grav_deceleration") is not None:
            UserPatch.patch_method("get_actor_grav_deceleration",
                                   local_dict.get("get_actor_grav_deceleration"),
                                   [float, int])
        if local_dict.get("get_actor_grav_high_jump") is not None:
            UserPatch.patch_method("get_actor_grav_high_jump",
                                   local_dict.get("get_actor_grav_high_jump"),
                                   [float, int])
        if local_dict.get("is_moving_up") is not None:
            UserPatch.patch_method("is_moving_up",
                                   local_dict.get("is_moving_up"),
                                   [float, int], 0)
