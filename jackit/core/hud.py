'''
Heads up display - Shows score, deaths, time, etc.
'''

import pygame

class Hud:
    '''
    Heads up display
    '''
    def __init__(self, game_engine):
        self.game_engine = game_engine

        # Init the font
        pygame.font.init()
        self.font = pygame.font.SysFont("Courier", 12)

        self.width = self.game_engine.screen_width
        self.height = self.font.get_linesize()

        # Setup the HUD rect
        self.hud_view = pygame.Surface([self.width, self.height])
        self.hud_view.fill((0, 0, 0)) # Black
        self.hud_view.set_alpha(240) # Pretty transparent
        self.hud_view = self.hud_view.convert()
        self.rect = self.hud_view.get_rect()

        # Put the HUD at the top left
        self.rect.x = 0
        self.rect.y = 0

        self.display_text_template = "Playtime: {0:.2f} | Points: {1} | Deaths: {2}"
        self.display_text = ""

    def update(self):
        '''
        Update the text
        '''
        self.display_text = self.display_text_template.format(
            self.game_engine.playtime,
            self.game_engine.total_points,
            self.game_engine.deaths
        )

    def draw(self, screen):
        '''
        Draw the HUD on the screen
        '''
        screen.blit(self.hud_view, self.rect)

        # Blit the display text with antialiasing = True and
        # Color of Green.
        screen.blit(self.font.render(
            self.display_text,
            True,
            (0, 255, 0)
        ), self.rect)
