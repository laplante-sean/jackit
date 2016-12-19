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
        print("\tPlaytime: {}s".format(GameEngine.playtime))
        print("\nFINAL WEIGHTED SCORE: ", GameEngine.final_score)
