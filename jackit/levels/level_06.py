'''
Fifth level
'''

from jackit.core.level import Level
from jackit.core.patch import UserPatch

class Level_06(Level):
    '''
    Sixth level - Break the game
    '''

    # pylint: disable=C0301
    _map = [
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "W                W                       W                    <<<<>>>>                    W           W          W            FFFFFFF",
        "W  S             W                   1   W   1                <<<<>>>>           0  5  0Z W           W          W            FFFFFFF",
        "W                W                   FFFFFFFFF                DDDDDDDD         FFFFFFFFFFFW           W          W            FFFFFFF",
        "W                W                   <<<<>>>>>                   W                        W           W          W            EEEEEEE",
        "W     p          W                   <<<<>>>>>    1 1 1   R      W         1 1 1 1        W     1     W     1   BW     1 1    EEEEEEE",
        "FFFFFcccFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    ]

    _challenge = """# Gotta go FAST!!!
# This time...Overdo it. Each block is 24x24 pixels
# and my collision detection isn't fancy

def get_top_speed():
    # Get the player's max speed in pixels/frame
    return {}

def get_x_acceleration():
    # Get the player's acceleration (added to current speed
    # on each frame until top_speed is reached)
    return {}

def get_x_deceleration():
    # Get the player's deceleration (subtracted from current
    # speed on each frame until the player stops)
    return {}"""

    def __init__(self, game_engine, player):
        super(Level_06, self).__init__(game_engine, Level_06._map, player)
        self.challenge = Level_06._challenge.format(
            player.stats.top_speed,
            player.stats.x_acceleration,
            player.stats.x_deceleration
        )

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_06, self).create_code_block(x_pos, y_pos)
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
        if local_dict.get("get_top_speed", None) is not None:
            UserPatch.patch_method("get_top_speed",
                                   local_dict.get("get_top_speed"),
                                   [float, int])
        if local_dict.get("get_x_acceleration") is not None:
            UserPatch.patch_method("get_x_acceleration",
                                   local_dict.get("get_x_acceleration"),
                                   [float, int])
        if local_dict.get("get_x_deceleration") is not None:
            UserPatch.patch_method("get_x_deceleration",
                                   local_dict.get("get_x_deceleration"),
                                   [float, int])
