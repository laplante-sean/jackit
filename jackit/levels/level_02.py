'''
Second level - Test level
'''

from jackit.core.level import Level

class Level_02(Level):
    '''
    Second level - Test level
    '''

    _map = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          PPPP",
        "P                             PP           P",
        "P                                          P",
        "P                 E                 PPPPPPPP",
        "P            PPPPPPPPPPP                   P",
        "                              PPPPPP        ",
        "     S                                      ",
        "                                            ",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    def __init__(self, game_engine):
        super(Level_02, self).__init__(game_engine, Level_02._map)

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_02, self).create_code_block(x_pos, y_pos)
        return block
