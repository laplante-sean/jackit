'''
Level 2
'''

from jackit.core.level import Level

class Level_02(Level):
    '''
    Second level - Test level
    '''

    _map = [
        "                                            ",
        "                                           WWWWWWWWWWWWWWWWWW",
        "                                           W                E",
        "                                           W 5              E",
        "                 WWWWWWWWWWWWWWWWWWWWWWWWWWWFFF          FFFW",
        "                 W                             FF           W",
        "                 W                                         BW",
        "                 W               1 1 1               FFFFFFFW",
        "                 W   S        FFFFFFFFFFF                   W",
        "                 W                             FFFFFFFF     W",
        "                                                            W",
        "                                                     B   B  W",
        "                 FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF            ",
        "        GGG                                                              ",
        "  5              1         1                                               ",
        "GGGGG           GGG       GGG                                             ",
        "                                                                                   ",
        "           1 1 1 1 1 1   Z                                            0              ",
        "       GGGGGGGGGGGGGGGGGGG                      1 1 1 1 1  B        WFFFF              ",
        "                                         GGGGGGGGGGGGGGGGGGGGGGGGGGGG              ",
        "                                                                                    ",
        "    Z5 5 5 5 5 5                                       ",
        "   GGGGGGGGGGGGGG          L 0  0  0  0     ",
        "                          GGGGGGGGGGGGGGGG  ",
        "                                            ",

    ]

    def __init__(self, game_engine, player):
        super(Level_02, self).__init__(game_engine, Level_02._map, player)

    def load(self):
        super(Level_02, self).load()
        self.game_engine.hud.display_popup("WATCH OUT! THEY RESPAWN!", 4)
