'''
Seventh level
'''

from jackit.core.level import Level
from jackit.core.patch import UserPatch

class Level_08(Level):
    '''
    Seventh level - Find the key
    '''

    # pylint: disable=C0301
    _map = [
        "                                                                  ",
        "                                                                  ",
        "                                                                  ",
        "                                                                  ",
        "                                               DDDDDDDDD          ",
        "                                            <>           <>       ",
        "                       0                    <>           <>       ",
        "                      GGG                   <>     5     <>                                                   ",
        "                                            <>     S     <>   000000000                                   ",
        "                                 E          <>     p     <>   000000000                                ",
        "           1 1               GGGGGGGGGG     <>   ccccc   <>   GGGGGGGGG                                     ",
        "         GGGGGGG                              ^^^^^^^^^^^                                                    ",
        "                G                                                                                                ",
        "                                                                                                               ",
        "                  1 1 1                                                                              ",
        "                GGGGGGGGGG           5             5             5                                  ",
        "                                   ZWWW B         WWW          RWWW  L                                 ",
        "                        GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                  ",
        "                                                                                                   ",
        "                                                                                                 ",
        "                                                                                                   ",
        "                                                                                                  "
    ]

    _challenge = """# Let's apply all we've
# learned...to figure this out...shit man!
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
        super(Level_08, self).__init__(game_engine, Level_08._map, player)
        self.challenge = Level_08._challenge.format(
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
        block = super(Level_08, self).create_code_block(x_pos, y_pos, locked)
        block.challenge_text = self.challenge
        return block

    def load(self):
        super(Level_08, self).load()
        self.game_engine.hud.display_popup("Well Shit!", 2)

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
