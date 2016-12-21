'''
The main game loop
'''

import os
import sys
import marshal
import requests

from deploy import SiteDeployment

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
        print("\tLevels Completed: ", GameEngine.levels_completed)

        if GameEngine.user is None or len(GameEngine.user.strip()) == 0:
            print("No username provided. Not submitting score. Enter username when game starts.")
            return

        print("Submitting score...")

        try:
            r = requests.post(
                GameEngine.config.leaderboard.submission_url,
                data={
                    'user': GameEngine.user,
                    'score':GameEngine.total_points,
                    'deaths':GameEngine.deaths,
                    'playtime':GameEngine.playtime,
                    'game_id': GameEngine.game_id,
                    'levels_completed': GameEngine.levels_completed
                }
            )
            print(r.status_code, r.reason)
        except BaseException as e:
            return
