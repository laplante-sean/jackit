'''
Handles a single line of text input
'''

from string import ascii_letters
import pygame

from jackit.core import CustomEvent
from jackit.core.editor import CodeEditor

class TextInput(CodeEditor):
    '''
    Brings up a box that handles a single line of text input
    '''
    def __init__(self, game_engine, max_chars=25):
        super(TextInput, self).__init__(game_engine)
        self.initial_edit = False
        self.max_chars = max_chars
        self.height = self.line_size
        self.width = int(
            self.font.size(ascii_letters)[0] / len(ascii_letters)) * max_chars

        # Setup the text box
        self.code_window = pygame.Surface([self.width, self.height])
        self.code_window.fill(self.config.bg_color)
        self.code_window.set_alpha(self.config.bg_alpha)
        self.code_window = self.code_window.convert()
        self.rect = self.code_window.get_rect()

        self.rect.x = (self.game_engine.screen_width - self.width) / 2
        self.rect.y = (self.game_engine.screen_height - self.height) / 2

        # Set initial position of the cursor
        self.cursor_rect.x = self.rect.x
        self.cursor_rect.y = self.rect.y

    def stop(self):
        '''
        Called when the user hits enter. Overrides the code editor version
        '''
        self.running = False
        pygame.event.post(pygame.event.Event(CustomEvent.SET_USER, {"text": self.text}))
        pygame.key.set_repeat() # Sets back to no repeat

    def update(self):
        '''
        Update cursor and stuff. Overrides the code editor version
        '''
        if not self.text_change:
            return

        if len(self.text) > self.max_chars:
            self.text = self.text[:self.max_chars]

        if self.cursor_position > len(self.text):
            self.cursor_position = len(self.text)

    def draw(self, screen):
        '''
        Draw the line editor. Overrides the code editor version
        '''

        # Wipe out the background
        screen.fill((0, 0, 0))

        # Blit the background window to the screen
        screen.blit(self.code_window, self.rect)

        if self.text_change:
            if len(self.text) > 0:
                w, _ = self.font.size(
                    self.text[:self.cursor_position]
                )
                self.cursor_rect.x = self.rect.x + w
            else:
                self.cursor_rect.x = self.rect.x

        try:
            screen.blit(self.font.render(
                self.text,
                self.config.font_antialiasing,
                self.config.font_color
            ), self.rect)
        except BaseException:
            screen.blit(self.font.render(
                "*"*len(self.text),
                self.config.font_antialiasing,
                self.config.font_color
            ), self.rect)

        screen.blit(self.cursor, self.cursor_rect)

        self.text_change = False

    def handle_event(self, event):
        '''
        Handle input events while the code editor is up.
        Overrides the code editor version
        '''
        if event.type == pygame.KEYDOWN:
            self.text_change = True

            if not self.initial_edit and event.key != pygame.K_RETURN:
                self.initial_edit = True
                self.text = ""

            if event.key == pygame.K_RETURN and self.initial_edit:
                self.stop()
            elif event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_DELETE:
                self.k_delete()
            elif event.key == pygame.K_LEFT:
                self.k_left()
            elif event.key == pygame.K_RIGHT:
                self.k_right()
            elif event.key == pygame.K_BACKSPACE:
                self.k_backspace()
            elif event.key == pygame.K_TAB:
                pass
            elif event.key == pygame.K_ESCAPE:
                pass
            else:
                self.character_key(event.key)

        return True # keep processing events
