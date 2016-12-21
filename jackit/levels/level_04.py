'''
Fourth level
'''

from jackit.core.level import Level
from jackit.core.patch import UserPatch

class Level_04(Level):
    '''
    Fourth level - Don't overdo it with the stats guy
    '''

    _map = [
        "             WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWDDDDDDDDDDDDDDDDDDDDDDDDDDDDW",
        "W5  S                                    <W",
        "W                                        <W",
        "W           c            1  1  1  1      <W",
        "WFFFFFFFFFFFFF         FFFFFFFFFFFF   FFFFW",
        "                               WWWW       E",
        "                               WWWW       E",
        "                               WWWWFFFFFFFW"
    ]

    _challenge = """# Make this jump!!
# Now there's some death spikes to keep you in line

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
        super(Level_04, self).__init__(game_engine, Level_04._map, player)

        self.challenge = Level_04._challenge.format(
            player.stats.top_speed,
            player.stats.jump_speed,
            player.stats.x_acceleration
        )

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_04, self).create_code_block(x_pos, y_pos)
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
        if local_dict.get("get_jump_speed") is not None:
            UserPatch.patch_method("get_jump_speed",
                                   local_dict.get("get_jump_speed"),
                                   [float, int])
        if local_dict.get("get_x_acceleration") is not None:
            UserPatch.patch_method("get_x_acceleration",
                                   local_dict.get("get_x_acceleration"),
                                   [float, int])
