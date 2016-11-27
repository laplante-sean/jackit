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
        from jackit.engine import GameEngine

        while True:
            GameEngine.update()
