'''
Does the sound for the game
'''

import os
import pygame

from deploy import SiteDeployment

class Sound:
    '''
    Handles all the sound for the game
    '''

    def __init__(self, game_engine):
        self.game_engine = game_engine
        game_music_path = os.path.join(SiteDeployment.resource_path, "sound", "music.mp3")
        pygame.mixer.music.load(game_music_path)

    def play_game_music(self):
        '''
        Play the game music
        '''
        pygame.mixer.music.play(loops=-1)