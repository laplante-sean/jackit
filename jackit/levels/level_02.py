'''
Second level - Test level
'''

from jackit.core.level import Level

class Level_02(Level):
    '''
    First level - Test level
    '''
    
    _map = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P            PPPPPPPPPPP                   P",
        "P                         PPPPPPPPPP       E",
        "P    S                                     E",
        "P                                          E",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    def __init__(self, game_engine):
        super(Level_02, self).__init__(game_engine, Level_02._map)
