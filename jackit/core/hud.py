'''
Heads up display - Shows score, deaths, time, etc.
'''

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

        self.hint_queue = deque()
        self.current_hint = None
        self.current_delay = 0

        # Maximum number of things in the queue before messages are dropped
        self.queue_spam_protection = 5

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

        if self.current_hint:
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
