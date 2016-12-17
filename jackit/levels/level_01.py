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
        "P      11111                               P                            PP                                       P",
        "P    PPPPPPPP                              P                            PPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                           1              P                                                                     P",
        "P                          PPPPPPP         P                                                                     P",
        "P                 PPPPPP                   P                             5                                       P",
        "P            1                             P           PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP                          P",
        "P         PPPPPPP                          P                                                                     P",
        "P                        1                 P                                                                     P",
        "P                     PPPPPP               P                                             1 1 1 1 1 1 1           P",
        "P                                          P                                      PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P   PPPPPPPPPPP                            P                                                                     P",
        "P                                          P                                                                     P",
        "P                 PPPPPPPPPPP              P                                                                     P",
        "P                                          P                                                                     P",
        "P                                          P                          111111111111111111111111111111             P",
        "P                               PPPPPPPPPPPP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P                                                                     E",
        "P                                          P                                                                     E",
        "P                        PPPPPPPPPPPPP     P                                                                     E",
        "P                                          P                                                                     E",
        "P                      000000000000000     PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P          PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P   0                                      P",
        "PPPPPP                                     P",
        "P     P                                    P",
        "P      P B                                 P",
        "P       PPP  5                             P",
        "P           PPP   5                        P",
        "P                PPP                       P",
        "P                        LLLLLLLLLL        P",
        "P                       PPPPPPPPPPP        P",
        "P                                          P",
        "P                  L                       P",
        "P            PPPPPPPPPPP                   P",
        "P                                          P",
        "P                             L            P",
        "P                         PPPPPPPPPP       E",
        "P    S                                     E",
        "P    C     K 1 1 1 1 1 C                   E",
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
