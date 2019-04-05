'''
Initial welcome page
'''

import pygame

INFO_TEMPLATE = """Complete levels to earn flags. Flags will
be printed in the console window.

Movement:
Left: 'A'
Right: 'D'
Jump: '<Space Bar>'

Code Blocks:
Interact: 'E'
Exit Editor: 'ESC'
Reset Code: 'Q'
Edit Text: Arrow keys + keyboard

Sound:
Toggle Music: 'M' (by: Jacob Hartman)

Quit: Close this window and then hit enter in the console window.
This way you don't miss any sweet flags.

Scores are submitted automatically on exit.
Check your score on https://jackit.io

May cause seizures. Don't blow it.

<Press ENTER to begin>"""

class Welcome:
    '''
    Initial welcome page
    '''
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.config = self.game_engine.config

        # Init the font
        pygame.font.init()
        self.welcome_font = pygame.font.SysFont("Courier", 26)
        self.info_font = pygame.font.SysFont("Courier", 16)

        self.welcome_line_size = self.welcome_font.get_linesize()
        self.info_line_size = self.info_font.get_linesize()

        self.width = self.game_engine.screen_width
        self.height = self.game_engine.screen_height

        self.welcome_view = pygame.Surface([self.width, self.height])
        self.welcome_view.fill((0, 0, 0)) # Black
        self.welcome_view = self.welcome_view.convert()
        self.rect = self.welcome_view.get_rect()

        self.welcome_text_rect = pygame.Rect(
            self.rect.x, self.rect.y, self.width, self.welcome_line_size)

        self.info_text_rect = pygame.Rect(
            self.rect.x, self.rect.y, self.width, self.info_line_size)

        self.welcome_text = "Welcome CNY Hackathon"
        self.info_template = INFO_TEMPLATE

        self.render_welcome_text = []
        self.render_info = []

        self.running = False

    def run(self):
        '''
        Run the welcome page
        '''
        self.running = True

    def is_running(self):
        '''
        Is the welcome page running
        '''
        return self.running

    def stop(self):
        '''
        Exit the welcome page
        '''
        self.running = False

    def update(self):
        '''
        Updates the welcome page
        '''
        self.welcome_text_rect.y = self.rect.y
        self.info_text_rect.y = self.rect.y

        self.render_info = []
        self.render_welcome_text = []
        for line in self.welcome_text.split("\n"):
            self.render_welcome_text.append(line)

        for line in self.info_template.split("\n"):
            self.render_info.append(line)

    def draw(self, screen):
        '''
        Draw the text to the screen
        '''
        screen.fill((0, 0, 0))

        screen.blit(self.welcome_view, self.rect)

        for line in self.render_welcome_text:
            screen.blit(self.welcome_font.render(
                line,
                True, # Antialiasing
                (0, 255, 0) # Green
            ), self.welcome_text_rect)

            self.welcome_text_rect.y += self.welcome_line_size

        self.info_text_rect.y = self.welcome_text_rect.y + self.welcome_line_size

        for line in self.render_info:
            screen.blit(self.info_font.render(
                line,
                True, # Antialiasing
                (0, 255, 0) # Green
            ), self.info_text_rect)

            self.info_text_rect.y += self.info_line_size

    def handle_event(self, event):
        '''
        Handle event
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.stop()
        return True
