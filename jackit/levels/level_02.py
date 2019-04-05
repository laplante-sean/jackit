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
        "                          WWWWWWWWWWWWWWWWWW",
        "                          W                E",
        "                          W 5              E",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWFFF          FFFW",
        "W                             FF           W",
        "W                                         BW",
        "W               1 1 1               FFFFFFFW",
        "W   S        FFFFFFFFFFF                   W",
        "W                             FFFFFFFF     W",
        "W                                          W",
        "W                                   B   B  W",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
    ]

    def __init__(self, game_engine, player):
        super(Level_02, self).__init__(game_engine, Level_02._map, player)

    def load(self):
        super(Level_02, self).load()
        self.game_engine.hud.display_popup("WATCH OUT! THEY RESPAWN!", 4)
