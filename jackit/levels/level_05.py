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
        "                                      PPPPPPDDDDDDDPP",
        "                                      P            <P",
        "                                      P            <P",
        "                                      P  PP        <P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP  <>        <PPPPPPPPPPPPPP",
        "P S           1   1   1   1   1          <> 000000 <>          EP",
        "P                                        <PPPPPPPPPP>          EP",
        "P    C                                   <PDDDDDDDDP>      PPPPPP",
        "PPPPPPP                                                         ",
        "                Z                   1   1   1                   ",
        "              PPPPPPPPPPP        PPPPPPPPPPPPPPP                ",
        "                                    5   0   5         1  1      ",
        "                                                   PPPPPPPPPP   ",
        "                                                      0000      ",
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
        "                                       1  5 1 5  1              ",
        "                                       PPPPPPPPPPP              "
    ]

    _challenge = """# There's items up there!
# There's items everywhere. Time to play with gravity!'

def get_grav_acceleration():
    # The force of gravity when the player is falling. Added to the 
    # players falling speed until terminal velocity is reached
    return {}

def get_grav_deceleration():
    # The force of gravity when the player is going up.
    # Subtracted from jump speed to slow the player down.
    # Once falling, grav_acceleration is used instead
    return {}

def get_grav_high_jump():
    # While the jump button is held and while is_moving_up()
    # is True, apply this value as grav_deceleration instead
    # of the default grav_deceleration
    return {}

def is_moving_up(change_y):
    # True if the player is moving up (up is negative)
    return change_y < 0

def is_moving_down(change_y):
    # True if the player is moving down (down is positive)
    return change_y > 0"""

    def __init__(self, game_engine, player):
        super(Level_05, self).__init__(game_engine, Level_05._map, player)
        self.challenge = Level_05._challenge.format(
            player.stats.grav_acceleration,
            player.stats.grav_deceleration,
            player.stats.grav_high_jump
        )

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_05, self).create_code_block(x_pos, y_pos)
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
            print("That's some bad code! ", str(e))

        # Patch the provided methods
        if local_dict.get("get_grav_acceleration", None) is not None:
            UserPatch.patch_method("get_grav_acceleration",
                                   local_dict.get("get_grav_acceleration"),
                                   [float, int])
        if local_dict.get("get_grav_deceleration") is not None:
            UserPatch.patch_method("get_grav_deceleration",
                                   local_dict.get("get_grav_deceleration"),
                                   [float, int])
        if local_dict.get("get_grav_high_jump") is not None:
            UserPatch.patch_method("get_grav_high_jump",
                                   local_dict.get("get_grav_high_jump"),
                                   [float, int])
        if local_dict.get("is_moving_up") is not None:
            UserPatch.patch_method("is_moving_up",
                                   local_dict.get("is_moving_up"),
                                   [bool], 0)
        if local_dict.get("is_moving_down") is not None:
            UserPatch.patch_method("is_moving_down",
                                   local_dict.get("is_moving_down"),
                                   [bool], 0)
