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
        "                                               PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "                                               P                                                                 P",
        "                                               P                                                                 P",
        "                                               P                                                                 P",
        "                                               P                                                                 P",
        "                                               P                                                                 P",
        "                                               P                                                                 P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP                  PPPPPPPP                                       P",
        "P                                                                        P                                       P",
        "P                                                  PPPPPPPP              P                                       P",
        "P                                                                        P                                       P",
        "P                    PPPPPPPPPPP                               PPPPPPPPPPP                                       P",
        "P                                                                        PPPPPPPPPPPPPPPPPPPPPPPPPPP             P",
        "P                                          PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP                                       P",
        "P                                          P                            PP                                       P",
        "P    PPPPPPPP                              P                            PPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P                                                                     P",
        "P                          PPPPPPP         P                                                                     P",
        "P                 PPPPPP                   P                                                                     P",
        "P                                          P           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP                          P",
        "P         PPPPPPP                          P                                                                     P",
        "P                                          P                                                                     P",
        "P                     PPPPPP               P                                                                     P",
        "P                                          P                                      PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P   PPPPPPPPPPP                            P                                                                     P",
        "P                                          P                                                                     P",
        "P                 PPPPPPPPPPP              P                                                                     P",
        "P                                          P                                                                     P",
        "P                                          P                                                                     P",
        "P                               PPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P                                                                     E",
        "P                                          P                                                                     E",
        "P                        PPPPPPPPPPPPP     P                                                                     E",
        "P                                          P                                 C                                   E",
        "P                                          PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P          PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "PPPPPP                                     P",
        "P     P                                    P",
        "P      P                                   P",
        "P       PPP                                P",
        "P           PPP                            P",
        "P                PPP                       P",
        "P                                          P",
        "P                       PPPPPPPPPPP        P",
        "P                                          P",
        "P                                          P",
        "P            PPPPPPPPPPP                   P",
        "P                                          P",
        "P                                  B       P",
        "P        MMMMMMMMM        PPPPPPPPPP       E",
        "P    S                                     E",
        "P    C                 C                   E",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    def __init__(self, game_engine):
        super(Level_01, self).__init__(game_engine, Level_01._map)

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_01, self).create_code_block(x_pos, y_pos)
        return block
