'''
User controllable player
'''

from jackit.core.actor import Actor

class Player(Actor):
    '''
    User controlled player
    '''

    def __init__(self, game_engine):
        super(Player, self).__init__(game_engine)

        self.walking_speed = 4
        self.running_speed = 6

        # TODO: Add stuff like health, items, etc.. to this class