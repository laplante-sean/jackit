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
        "P   0                                                     P",
        "PPPPPPPPP                                                 P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                      1                                  P",
        "P                     1                                   P",
        "P                    1                                    P",
        "P                   1                                     P",
        "P                  1                                      P",
        "P                 1                                       P",
        "P                1                                        P",
        "P               1                                         P",
        "P              1                                          P",
        "P             1                                           E",
        "PS          C1                                            E",
        "PPPPPPPPPPPPPP                 PPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    _challenge = """# Make the jump!
# But don't overdo it. Each block is 24x24 pixels
# and my collision detection isn't fancy

def get_top_speed():
    # Get the player's max speed in pixels/frame
    return {}

def get_jump_speed():
    # Get the player's max jump speed in pixels/frame
    return {}

def get_x_acceleration():
    # Get the player's acceleration (added to current speed
    # on each frame until top_speed is reached)
    return {}"""

    def __init__(self, game_engine, player):
        super(Level_03, self).__init__(game_engine, Level_03._map, player)

        self.challenge = Level_03._challenge.format(
            player.stats.top_speed,
            player.stats.jump_speed,
            player.stats.x_acceleration
        )

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_03, self).create_code_block(x_pos, y_pos)
        block.challenge_text = self.challenge
        return block

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
            # TODO: Display this as a popup
            print("That's some bad code! ", str(e))

        # Patch the provided methods
        if local_dict.get("get_top_speed", None) is not None:
            UserPatch.patch_method("get_top_speed",
                                   local_dict.get("get_top_speed"),
                                   [float, int])
        if local_dict.get("get_jump_speed") is not None:
            UserPatch.patch_method("get_jump_speed",
                                   local_dict.get("get_jump_speed"),
                                   [float, int])
        if local_dict.get("get_x_acceleration") is not None:
            UserPatch.patch_method("get_x_acceleration",
                                   local_dict.get("get_x_acceleration"),
                                   [float, int])
