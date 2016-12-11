'''
Code to display text boxes
'''

import textwrap
from string import ascii_letters

import pygame

class TextBox:
    '''
    Configurable text box
    '''
    def __init__(self, game_engine,
                 x_pos, y_pos, width, height,
                 text_color=(0, 0, 0), bg_color=(255, 255, 255),
                 antialiasing=True, font="Courier", font_size=16):
        self.game_engine = game_engine
        self.width = width
        self.height = height
        self.text_color = text_color
        self.bg_color = bg_color
        self.antialiasing = antialiasing
        self.font = font
        self.font_size = font_size
