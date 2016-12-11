'''
Level 3
'''

from jackit.core.level import Level

class Level_03(Level):
    '''
    Long jump - Introduction to coding
    '''

    _map = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         E",
        "P                                                         E",
        "PS          C                                             E",
        "PPPPPPPPPPPPPP                             PPPPPPPPPPPPPPPP",
    ]

    def __init__(self, game_engine):
        self.code_blocks = []
        super(Level_03, self).__init__(game_engine, Level_03._map)

    def create_code_block(self, x_pos, y_pos):
        block = super(Level_03, self).create_code_block(x_pos, y_pos)
        self.code_blocks.append(block)
        return block

    def setup_level(self):
        '''
        Setup the challenges
        '''
        super(Level_03, self).setup_level()

        self.code_blocks[0].challenge_text = """# Make the jump!
def get_player_top_speed():
    # Called to get the players current top speed
    return {}

def get_player_jump_speed():
    # Called to get the players current y-axis top speed
    return {}

def get_player_x_acceleration():
    # Called to get the players x-axis acceleration
    return {}
        """.format(
            self.game_engine.player.stats.top_speed,
            self.game_engine.player.stats.jump_speed,
            self.game_engine.player.stats.x_acceleration
        )

    def get_player_top_speed(self):
        '''
        Getter for player top speed
        '''
        return self.game_engine.player.stats.top_speed

    def get_player_jump_speed(self):
        '''
        Getter for player jump speed
        '''
        return self.game_engine.player.stats.jump_speed

    def get_player_x_acceleration(self):
        '''
        Getter for player x-axis acceleration
        '''
        return self.game_engine.player.stats.x_acceleration
