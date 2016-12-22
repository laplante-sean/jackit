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
        "                                                    S                                                       ",
        "  00000000                                                                                                  ",
        "  00000000                                                                                                  ",
        "  00000000                                                                                                  ",
        "  00000000                                                                                                  ",
        "                                                                          5                                 ",
        "                                                                         GGG                                ",
        "                                                                  K                                         ",
        "                                                               ^GGGGG^            L                          ",
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
        ">      0       1  1  1  1  1  1  1  1                                   1  GGFFFFFFFFFFFFFFFFFFFFFFFF^^^^^^^^^^^^^^^^^^^^^^",
        ">      5                                                          1  GGGGGGDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
        ">      5                                             X          GGGGGG        <                                            ",
        ">      0           ^^^^^^^^^^^^^^^^^^^^^^^^^GGGGGGGGcccGGGGGGGGG              <                                            ",
        ">      5           DDDDDDDDDDDDDDDDDDDDDDDDD        EEE                       <                                            ",
        ">      0                                            EEE                       <                                            ",
        ">      5                                             0                        <                                            ",
        ">      0       1 1 1                                 5                        <                                            ",
        ">      0   5            5  1111111111                                         <                                            ",
        ">  GGGGGGGGGG    X     GGGGGGGGGGGGGGG^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                             ",
        ">               ccc                                                                                                        ",
        " ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                                                                                     ",
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

    _challenge = """# Let's apply all we've
# learned...to fly! Don't forget about 'Q' to reset
def get_terminal_velocity():
    return {}
def get_top_speed():
    return {}
def get_jump_speed():
    return {}
def get_x_acceleration():
    return {}
def get_x_deceleration():
    return {}
def get_grav_acceleration():
    return {}
def get_grav_deceleration():
    return {}
def get_grav_high_jump():
    return {}
def is_moving_up(change_y):
    return change_y < 0
def is_moving_down(change_y):
    return change_y > 0"""

    def __init__(self, game_engine, player):
        super(Level_07, self).__init__(game_engine, Level_07._map, player)
        self.challenge = Level_07._challenge.format(
            player.stats.terminal_velocity,
            player.stats.top_speed,
            player.stats.jump_speed,
            player.stats.x_acceleration,
            player.stats.x_deceleration,
            player.stats.grav_acceleration,
            player.stats.grav_deceleration,
            player.stats.grav_high_jump
        )

    def create_code_block(self, x_pos, y_pos, locked=False):
        block = super(Level_07, self).create_code_block(x_pos, y_pos, locked)
        block.challenge_text = self.challenge
        return block

    def load(self):
        super(Level_07, self).load()
        self.game_engine.hud.display_popup("Was that a key up there? Damn encrypted code!", 4)

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
        if local_dict.get("get_top_speed", None) is not None:
            UserPatch.patch_method("get_top_speed",
                                   local_dict.get("get_top_speed"),
                                   [float, int])
        if local_dict.get("get_jump_speed") is not None:
            UserPatch.patch_method("get_jump_speed",
                                   local_dict.get("get_jump_speed"),
                                   [float, int])
