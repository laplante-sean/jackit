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
        "P                         K                                     U        P                                       P",
        "P                    PPPPPPPPPPP                               PPPPPPPPPPP            5 5 5 5                    P",
        "P                                                                        PPPPPPPPPPPPPPPPPPPPPPPPPPP             P",
        "P                                          PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP                                       P",
        "P        B                                 P                            PP                                       P",
        "P    PPPPPPPP                              P                            PPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P                                                                     P",
        "P                          PPPPPPP         P                                                                     P",
        "P                 PPPPPP                   P                             5                                       P",
        "P                                          P           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP                          P",
        "P         PPPPPPP                          P                                                                     P",
        "P                                          P                                                                     P",
        "P                     PPPPPP               P                                             1 1 1 1 1 1 1     Z     P",
        "P                                          P                                      PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P   PPPPPPPPPPP                            P                                                                     P",
        "P                       L                  P                                                                     P",
        "P                 PPPPPPPPPPP              P                                                                     P",
        "P                                          P                                                                     P",
        "P                                          P                                                  Z                  P",
        "P                               PPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P                                                                     E",
        "P                                          P                                                                     E",
        "P                        PPPPPPPPPPPPP     P                                                                     E",
        "P                                          P                                          B                          E",
        "P                                Z         PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P          PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P   0                                      P",
        "PPPPPP                                     P",
        "P     P                                    P",
        "P      P                                   P",
        "P       PPP  5                             P",
        "P           PPP   5                        P",
        "P                PPP                       P",
        "P                                          P",
        "P                       PPPPPPPPPPP        P",
        "P                                          P",
        "P              L                           P",
        "P            PPPPPPPPPPP                   P",
        "P                                          P",
        "P                                          P",
        "P                         PPPPPPPPPP       E",
        "P    S                                     E",
        "P    C     K 1 1 1 1 1 C         R         E",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    def __init__(self, game_engine):
        super(Level_01, self).__init__(game_engine, Level_01._map)

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_01, self).create_code_block(x_pos, y_pos)
        block.challenge_text = """
dDDDdjslkfjdsf;lksafhkfjahsdjkfhasdkjfhalsdkjfhaldjksfhalkjsdhflakjshdflkajhfldkajhdlkjhalkjsdhflasjdhfalksdjhfaldsj
        """
        block.locked = True
        return block
