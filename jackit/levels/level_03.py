'''
Level 3
'''

from jackit.core.level import Level
from jackit.core.patch import UserPatch

class Level_03(Level):
    '''
    Long jump - Introduction to coding
    '''

    # pylint: disable=C0301
    _map = [
        "                                                                   ",
        "                                                                   ",
        "                                                                   ",
        "                                                                   ",
        "                                                                   ",
        "                0 0                                                ",
        "            CCCCCCCCCCC                                            ",
        "                                                                   ",
        "                             L                                     ",
        "                          CCCCCCCCCC                               ",
        "                                                    Z              ",
        "                                         CCCCCCCCCCCCCCCC          ",
        "                                                                   ",
        "                                                                   ",
        "                                                                   ",
        "                                                                   ",
        "                                              5           5        ",
        "CC       CCCC       CCCCCCCC    CCCCC        CCC         CC      CC",
        "                                                                   ",
        "    0                                                              ",
        "CCCCCCCCC                                 ^^^^^^^^^^^^^^^^^^^^^^^  ",
        "                                          DDDDDDDDDDDDDDDDDDDDDDD  ",
        "                                                                   ",
        "                                                                   ",
        "                                                                                            1 5 1            ",
        "                                                                                          CCCCCCCCC          ",
        "                                                                           F       CCC                       ",
        "                        1                                                 FFF                                ",
        "                       1                                                FFFFFFF                              ",
        "                      1                                              FFFFFFFFFFFFF                           ",
        "                     1                                              FF           FF                          ",
        "                    1                                              FF   0      0  FF                         ",
        "W                  1                                              WWWWWWWWWW  WWWWWWW                        ",
        "W                 1                                               W                 W                        ",
        "W   S            1                                                W                 W                        ",
        "W               1                                                 W                 W                        ",
        "W              1                                                                   EW                        ",
        "W            p1                                                                    EW     5    1 1 1 1  0    ",
        "GGGGGGGGGGGGcccG                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
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

        self.has_reset_once = False

        self.challenge = Level_03._challenge.format(
            player.stats.top_speed,
            player.stats.jump_speed,
            player.stats.x_acceleration
        )

    def load(self):
        super(Level_03, self).load()
        self.game_engine.hud.display_popup("That thing over there that looks like tech. Press 'E' to jack on and 'ESC' to jack off!", 6)

    def reset(self):
        super(Level_03, self).reset()
        if not self.has_reset_once:
            self.has_reset_once = True
            self.game_engine.hud.display_popup("OUCH! Your code changes stick around b/w deaths. Press 'Q' to reset", 4)

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
