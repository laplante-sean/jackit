'''
The main game loop
'''

import sys
import requests

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

        print("Game over {}: ".format(GameEngine.user))
        print("\tScore: ", GameEngine.total_points)
        print("\tDeaths: ", GameEngine.deaths)
        print("\tPlaytime: {0:.2f}s".format(GameEngine.playtime))

        print("Submitting score...")

        r = requests.post(
            GameEngine.config.leaderboard.submission_url,
            data={
                'user': GameEngine.user,
                'score':GameEngine.total_points,
                'deaths':GameEngine.deaths,
                'playtime':GameEngine.playtime
            }
        )

        print(r.status_code, r.reason)
