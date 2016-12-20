'''
Level 2
'''

from jackit.core.level import Level

class Level_02(Level):
    '''
    Second level - Test level
    '''

    _map = [
        "                          PPPPPPPPPPPPPPPPPP",
        "                          P                E",
        "                          P 0              E",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP          PPPP",
        "P                             PP           P",
        "P                                         BP",
        "P               1 1 1               PPPPPPPP",
        "P   S        PPPPPPPPPPP                   P",
        "P                             PPPPPPPP     P",
        "                                           P",
        "                                    B   B  P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    def __init__(self, game_engine, player):
        super(Level_02, self).__init__(game_engine, Level_02._map, player)
