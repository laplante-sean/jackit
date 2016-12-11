'''
Third level level - Test level with actual coding challenge
'''

from jackit.core.level import Level

class Level_03(Level):
    '''
    Third level - Test level
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

    def __init__(self, game_engine):
        super(Level_03, self).__init__(game_engine, Level_03._map)

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_03, self).create_code_block(x_pos, y_pos)

        block.challenge_text = """
# Make the jump!

def get_player_top_speed():
    '''
    Called to get the players current top speed
    '''
    return 6

def get_player_jump_speed():
    '''
    Called to get the players current y-axis top speed
    '''
    return 8
        """

        return block
