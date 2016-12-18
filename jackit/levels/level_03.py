'''
Level 3
'''

from jackit.core.level import Level
from jackit.core.patch import UserPatch

class Level_03(Level):
    '''
    Long jump - Introduction to coding
    '''

    _map = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         E",
        "P                                                         E",
        "PS          C                                             E",
        "PPPPPPPPPPPPPP                             PPPPPPPPPPPPPPPP",
    ]

    _challenges = [
        """# Make the jump!
def get_actor_top_speed():
    # Called to get the players current top speed
    return 0

def get_actor_jump_speed():
    # Called to get the players current y-axis top speed
    return 0

def get_actor_x_acceleration():
    # Called to get the players x-axis acceleration
    return 0
        """,
    ]

    def __init__(self, game_engine, player):
        super(Level_03, self).__init__(game_engine, Level_03._map, player)
        self.num_code_blocks_created = 0

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_03, self).create_code_block(x_pos, y_pos)

        block.challenge_text = Level_03._challenges[self.num_code_blocks_created]
        self.num_code_blocks_created += 1

        return block

    def unload(self):
        super(Level_03, self).unload()
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
        if local_dict.get("get_actor_top_speed", None) is not None:
            UserPatch.patch_method("get_actor_top_speed",
                                   local_dict.get("get_actor_top_speed"),
                                   [float, int])
        if local_dict.get("get_actor_jump_speed") is not None:
            UserPatch.patch_method("get_actor_jump_speed",
                                   local_dict.get("get_actor_jump_speed"),
                                   [float, int])
        if local_dict.get("get_actor_x_acceleration") is not None:
            UserPatch.patch_method("get_actor_x_acceleration",
                                   local_dict.get("get_actor_x_acceleration"),
                                   [float, int])
