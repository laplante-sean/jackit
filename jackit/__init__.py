'''
The main game loop
'''

import sys
import pygame

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
        print("\tScore: ", GameEngine.total_score)
        print("\tPlaytime: {}s".format(GameEngine.playtime))
