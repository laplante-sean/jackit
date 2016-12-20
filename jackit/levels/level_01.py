'''
Level 1
'''

from jackit.core.level import Level

class Level_01(Level):
    '''
    Basic moving around and killing the things
    '''

    # pylint: disable=C0301
    _map = [
        "PPPPPPPPPPPPPPPPPPPPPPP",
        "P                     P",
        "P                     P",
        "P                     E",
        "P               1     E",
        "P          PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "PPPPPP                                     P",
        "P     P                                    P",
        "P      P                                   P",
        "P       PPP  1                             P",
        "P           PPP                            P",
        "P                PPP                       P",
        "P                          1   1           P",
        "P                       PPPPPPPPPPP        P",
        "P                                          P",
        "P            L                             P",
        "P            PPPPPPPPPPP                   P",
        "P                                          P",
        "P    S                      1 1 1          P",
        "P                         PPPPPPPPPP       P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    def __init__(self, game_engine, player):
        super(Level_01, self).__init__(game_engine, Level_01._map, player)
