'''
Seventh level
'''

from jackit.core.level import Level
from jackit.core.patch import UserPatch

class Level_07(Level):
    '''
    Seventh level - Find the key
    '''

    # pylint: disable=C0301
    _map = [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                          5                                 ",
        "                                                                         GGG                                ",
        "                                                     S            K                                         ",
        "                                                                ^GGG^            L                          ",
        "                                                                DDDDD     GGGGGGGGGGGGG                     ",
        "                                                                                                            ",
        "                                                                                               1 1 1 1 1    ",
        "                                                                                              GGGGGGGGGGG   ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                   Z                        ",
        "                                                                             GGGGGGGGGGGG                   ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                1 1 1       ",
        "                                                                                             GGGGGGGGGG     ",
        "                                                                                                            ",
        "                                                                                    5                       ",
        ">                                                                                 WWWWW           WWW                      ",
        ">                                                                                 W                 W                      ",
        ">                                                                                 W                 W0                     ",
        ">                                                                                 W           WWWWWWWWW                    ",
        ">                                                                                                   W           0          ",
        ">                                                                              W        B           W          FFF         ",
        ">                                                                       1  GGFFFFFFFFFFFFFFFFFFFFFFFF^^^^^^^^^^^^^^^^^^^^^^",
        ">                                                                 1  GGGGGGDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
        ">                                                    X          GGGGGG        <                                            ",
        ">              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^GGGGGGGGCCCGGGGGGGGG              <                                            ",
        ">              DDDDDDDDDDDDDDDDDDDDDDDDDDDDD         E                        <                                            ",
        ">                                                                             <                                            ",
        ">                                                                             <                                            ",
        ">                                                                             <                                            ",
        ">                                                                             <                                            ",
        ">                                                                             <                                            ",
        ">                                                                             <                                            ",
        " ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                             ",
        "                                                                                                                           ",
        "                                                                                                                           ",
        "                                                                                                                           ",
        "                                                                                                                           ",
        "                                                                                                                           ",
        "                                                                                                                           ",
        "                                                                                                                           ",
        "                                                                                                                           ",
        "                                                                                                                           "
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
        super(Level_07, self).__init__(game_engine, Level_07._map, player)
        self.challenge = Level_07._challenge.format(
            player.stats.top_speed,
            player.stats.x_acceleration,
            player.stats.x_deceleration
        )

    def create_code_block(self, x_pos, y_pos, locked=False):
        block = super(Level_07, self).create_code_block(x_pos, y_pos, locked)
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
