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
        self.playing = False

    def is_playing(self):
        '''
        Getter for instance variable playing
        '''
        return self.playing

    def play_game_music(self):
        '''
        Play the game music
        '''
        pygame.mixer.music.play(loops=-1)
        self.playing = True

    def pause_game_music(self):
        '''
        Pause the game music
        '''
        pygame.mixer.music.pause()
        self.playing = False

    def toggle_game_music(self):
        '''
        Toggle the game music on and off
        '''
        if self.is_playing():
            self.pause_game_music()
        else:
            self.play_game_music()