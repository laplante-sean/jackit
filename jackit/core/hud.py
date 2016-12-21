'''
Heads up display - Shows score, deaths, time, etc.
'''

import textwrap
from string import ascii_letters
from collections import deque
import pygame

class Hud:
    '''
    Heads up display
    '''
    def __init__(self, game_engine):
        self.game_engine = game_engine

        # Init the font
        pygame.font.init()
        self.font = pygame.font.SysFont("Courier", 14)

        self.width = self.game_engine.screen_width
        self.height = self.font.get_linesize()

        # Setup the HUD rect
        self.hud_view = pygame.Surface([self.width, self.height])
        self.hud_view.fill((0, 0, 0)) # Black
        self.hud_view.set_alpha(240) # Pretty transparent
        self.hud_view = self.hud_view.convert()
        self.rect = self.hud_view.get_rect()

        self.display_text_template = "Playtime: {0:.2f} | Points: {1} | Deaths: {2}"
        self.display_text = ""

        # Init Hint stuff
        self.hint_queue = deque()
        self.current_hint = None
        self.current_delay = 0

        # Init popup stuff
        self.popup_queue = deque()
        self.current_popup = None
        self.current_popup_delay = 0
        self.popup_text = ""

        # Maximum number of things in the queue before messages are dropped
        self.queue_spam_protection = 5

        # Init the popup rect
        self.popup = None
        self.popup_rect = None
        self.popup_height = self.height
        self.popup_width = self.game_engine.screen_width / 3.5
        self.popup_max_chars = int(
            (self.popup_width / (self.font.size(ascii_letters)[0] / len(ascii_letters))) - 1)

        # Create the text wrapper for popups
        self.textwrapper = textwrap.TextWrapper(
            width=self.popup_max_chars,
            break_long_words=True,
            replace_whitespace=False,
            expand_tabs=False,
            drop_whitespace=False
        )

    def display_popup(self, message, delay=2):
        '''
        Add a popup to the screen
        '''
        if len(self.popup_queue) >= self.queue_spam_protection:
            return
        self.popup_queue.append({"message":message, "delay":delay})

    def display_hint(self, hint, delay=2):
        '''
        Add a hint to the hint display queue
        '''
        if len(self.hint_queue) >= self.queue_spam_protection:
            return
        self.hint_queue.append({"hint":hint, "delay":delay})

    def update(self):
        '''
        Update the text
        '''
        self.display_text = self.display_text_template.format(
            self.game_engine.playtime,
            self.game_engine.total_points,
            self.game_engine.deaths
        )

        if self.current_hint is not None:
            self.current_delay += (self.game_engine.clock.get_time() / 1000.0)
            if self.current_delay <= self.current_hint["delay"]:
                self.display_text += " | " + self.current_hint["hint"]
            else:
                self.current_hint = None
                self.current_delay = 0
        elif len(self.hint_queue) > 0:
            self.current_hint = self.hint_queue.popleft()
            self.current_delay = 0
            self.display_text += " | " + self.current_hint["hint"]

        if self.current_popup is not None:
            self.current_popup_delay += (self.game_engine.clock.get_time() / 1000.0)
            if self.current_popup_delay <= self.current_popup["delay"]:
                self.popup_text = self.textwrapper.wrap(self.current_popup["message"])
            else:
                self.current_popup = None
                self.popup = None
                self.popup_rect = None
                self.current_popup_delay = 0
        elif len(self.popup_queue) > 0:
            self.current_popup = self.popup_queue.popleft()
            self.current_popup_delay = 0
            self.popup_text = self.textwrapper.wrap(self.current_popup["message"])

    def draw(self, screen):
        '''
        Draw the HUD on the screen
        '''
        screen.blit(self.hud_view, self.rect)

        # Blit the display text with antialiasing = True and
        # Color of Green.
        screen.blit(self.font.render(
            self.display_text,
            self.game_engine.config.code_editor.font_antialiasing,
            self.game_engine.config.code_editor.font_color
        ), self.rect)

        if self.current_popup is not None:
            if self.popup is None:
                self.popup_height = (self.height * len(self.popup_text))
                self.popup = pygame.Surface([self.popup_width, self.popup_height])
                self.popup.fill(self.game_engine.config.code_editor.bg_color)
                self.popup.set_alpha(self.game_engine.config.code_editor.bg_alpha)
                self.popup = self.popup.convert()
            if self.popup_rect is None:
                self.popup_rect = self.popup.get_rect()
            
            # Keep the rect above the player even while the camera moves
            self.popup_rect.x =\
                self.game_engine.player.rect.x + self.game_engine.current_level.camera.state.left

            self.popup_rect.y =\
                ((self.game_engine.player.rect.y - self.popup_height) - 5) + self.game_engine.current_level.camera.state.top

            popup_text_rect = pygame.Rect(self.popup_rect.x, self.popup_rect.y, self.popup_width, self.popup_height)

            # Blit the popup background
            screen.blit(self.popup, self.popup_rect)

            for line in self.popup_text:
                screen.blit(self.font.render(
                    line,
                    self.game_engine.config.code_editor.font_antialiasing,
                    self.game_engine.config.code_editor.font_color
                ), popup_text_rect)

                popup_text_rect.y += self.height # height is the line_size in this class
