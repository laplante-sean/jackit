'''
The main game loop
'''

import sys

class JackitGame:
    '''
    JackIt Game class
    '''

    @staticmethod
    def run():
        '''
        Run the game
        '''
        from jackit.core.engine import GameEngine

        while GameEngine.running:
            GameEngine.update()

        print("Game over: ")
        print("\tScore: ", GameEngine.total_points)
        print("\tDeaths: ", GameEngine.deaths)
        print("\tPlaytime: {0:.2f}s".format(GameEngine.playtime))
