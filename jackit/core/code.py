'''
Code text editor
'''

import pygame

BLACK = (0, 0, 0)

class CodeEditor:
    '''
    Code view text editor
    '''

    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.running = False
        
        self.width = self.game_engine.screen_width / 1.25
        self.height = self.game_engine.screen_height / 1.25

        # 255 is 100% opaque 0 is 100% transparent
        self.code_editor_alpha = 210

        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.code_window = pygame.Surface([self.width, self.height])
        self.code_window.fill(BLACK)
        self.code_window.set_alpha(self.code_editor_alpha)
        self.code_window = self.code_window.convert() # Convert the image for faster blitting
        self.rect = self.code_window.get_rect()

        # Put the code editor window in the center
        self.rect.x += (self.game_engine.screen_width - self.width) / 2
        self.rect.y += (self.game_engine.screen_height - self.height) / 2

    def run(self):
        '''
        Setter for running instance variable
        '''
        self.running = True

    def is_running(self):
        '''
        Getter for running instance variable
        '''
        return self.running

    def update(self):
        '''
        Update for code editor
        '''
        pass

    def draw(self, screen):
        '''
        Draw the code editor
        '''
        screen.blit(self.code_window, self.rect)

    def handle_event(self, event, keys):
        '''
        Handle input events while the code editor is up
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Quiting out of code editor")
                self.running = False

        for _ in keys:
            pass
