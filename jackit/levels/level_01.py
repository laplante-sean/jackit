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
        "WWWWWWWWWWWWWWWWWWWWWWW",
        "W                     W",
        "W                     W",
        "W                     E",
        "W               1     E",
        "W          FFFFFFFFFFFWWWWWWWWWWWWWWWWWWWWWW",
        "W                                          W",
        "WFFFFF                                     W",
        "W     F                                    W",
        "W      F                                   W",
        "W       FFF  1                             W",
        "W           FFF                            W",
        "W                FFF                       W",
        "W                          1   1           W",
        "W                       FFFFFFFFFFF        W",
        "W                                          W",
        "W            L                             W",
        "W            FFFFFFFFFFF                   W",
        "W                                          W",
        "W    S                      1 1 1          W",
        "W                         FFFFFFFFFF       W",
        "W                                          W",
        "W                                          W",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
    ]

    def __init__(self, game_engine, player):
        super(Level_01, self).__init__(game_engine, Level_01._map, player)

    def load(self):
        super(Level_01, self).load()
        self.game_engine.hud.display_popup("Welcome to JackIT. 'A', 'D' to move. 'Space'' to jump. Have Fun!!!!!", 5)
        self.game_engine.hud.display_popup("The exit blocks are red. Run into them to move on.", 3)