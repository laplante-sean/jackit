'''
Code text editor
'''

import pygame

from jackit.core import CustomEvent

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class CodeEditor:
    '''
    Code view text editor
    '''
    def __init__(self, game_engine):
        # Setup font stuff
        pygame.font.init()
        self.font_object = pygame.font.Font(None, 18)

        self.game_engine = game_engine
        self.running = False
        self.message = None

        self.width = self.game_engine.screen_width / 1.25
        self.height = self.game_engine.screen_height / 1.25

        # TODO: Make these options in config
        # 255 is 100% opaque 0 is 100% transparent
        self.background_alpha = 210
        self.background_color = BLACK
        self.font_antialiasing = True
        self.font_color = GREEN

        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.code_window = pygame.Surface([self.width, self.height])
        self.code_window.fill(self.background_color)
        self.code_window.set_alpha(self.background_alpha)
        self.code_window = self.code_window.convert() # Convert the image for faster blitting
        self.rect = self.code_window.get_rect()

        # Put the code editor window in the center
        self.rect.x += (self.game_engine.screen_width - self.width) / 2
        self.rect.y += (self.game_engine.screen_height - self.height) / 2

        # Font rect. Moves down as lines are rendered
        self.font_rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)

        # The current position of the cursor
        self.cursor_position = 0
        self.cursor_blink_delay = 500
        self.ms_since_last_blink = 0    # Time since last cursor blink
        self.cursor_toggle = False
        self.cursor_width = 5
        self.cursor_color = WHITE
        self.cursor_alpha = 175

        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.cursor = pygame.Surface([self.cursor_width, self.font_object.get_linesize()])
        self.cursor.fill(self.cursor_color)
        self.cursor.set_alpha(self.cursor_alpha)
        self.cursor = self.cursor.convert() # Convert the image for faster blitting
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.x = self.rect.x
        self.cursor_rect.y = self.rect.y

        # Key delay for when a key is held (in milliseconds)
        self.key_delay = 150
        self.ms_since_last_key_action = 0   # Time since last key action
        self.last_tick_value = 0            # Last value of get_ticks()

    def run(self, start_text="Test line 1\nTest line 2\n"):
        '''
        Setter for running instance variable
        '''
        self.running = True
        self.message = start_text
        self.last_tick_value = pygame.time.get_ticks()

    def is_running(self):
        '''
        Getter for running instance variable
        '''
        return self.running

    def update(self):
        '''
        Update for code editor
        '''
        self.font_rect.y = self.rect.y # Reset the Y position (moves down with each line in draw())

        self.ms_since_last_key_action += (pygame.time.get_ticks() - self.last_tick_value)
        self.ms_since_last_blink += (pygame.time.get_ticks() - self.last_tick_value)
        self.last_tick_value = pygame.time.get_ticks()

        if self.ms_since_last_blink >= self.cursor_blink_delay:
            if self.cursor_toggle:
                self.cursor_toggle = False
            else:
                self.cursor_toggle = True

    def draw(self, screen):
        '''
        Draw the code editor
        '''
        screen.blit(self.code_window, self.rect)

        if self.message is not None and len(self.message):
            for line in self.message.split("\n"):
                screen.blit(self.font_object.render(
                    line,
                    self.font_antialiasing,
                    self.font_color
                ), self.font_rect)

                self.font_rect.y += self.font_object.get_linesize()

        #Calc cursor position
        if self.message[self.cursor_position] == "\n":
            self.cursor_rect.y += self.font_object.get_linesize()
            self.cursor_rect.x = self.rect.x #Reset back to the left
            self.cursor_position += 1

        w, _ = self.font_object.size(self.message[0:self.cursor_position])
        self.cursor_rect.x = self.rect.x + w

        #Draw the cursor
        if self.cursor_toggle:
            screen.blit(self.cursor, self.cursor_rect)

    def k_delete(self):
        '''
        Handles the delete key
        '''
        self.message = self.message[0:self.cursor_position] \
            + self.message[self.cursor_position + 1:]

    def k_backspace(self):
        '''
        Handles the backspace key
        '''
        if self.cursor_position > 0:
            self.message = self.message[0:self.cursor_position - 1] \
                + self.message[self.cursor_position:]
            self.cursor_position -= 1

    def k_left(self):
        '''
        Handles the left arrow key
        '''
        if self.cursor_position > 0:
            self.cursor_position -= 1

    def k_right(self):
        '''
        Handles the right arrow key
        '''
        if self.cursor_position < len(self.message) - 1:
            self.cursor_position += 1

    def handle_events(self, events, keys):
        '''
        Handle input events while the code editor is up
        '''
        got_keydown_event = False
        got_keyup_event = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.ms_since_last_key_action = 0
                got_keydown_event = True

                if event.key == pygame.K_ESCAPE:
                    print("Quiting out of code editor")
                    self.running = False
                    self.message = None
                elif event.key == pygame.K_DELETE:
                    self.k_delete()
                elif event.key == pygame.K_LEFT:
                    self.k_left()
                elif event.key == pygame.K_RIGHT:
                    self.k_right()
                elif event.key == pygame.K_BACKSPACE:
                    self.k_backspace()

            if event.type == pygame.KEYUP:
                self.ms_since_last_key_action = 0
                got_keyup_event = True

        if not got_keydown_event and not got_keyup_event:
            if self.ms_since_last_key_action >= self.key_delay:
                self.ms_since_last_key_action = 0

                # use if, elif, elif, ... to prevent needing to deal with multiple keys at once
                if keys[pygame.K_DELETE]:
                    self.k_delete()
                elif keys[pygame.K_LEFT]:
                    self.k_left()
                elif keys[pygame.K_RIGHT]:
                    self.k_right()
                elif keys[pygame.K_BACKSPACE]:
                    self.k_backspace()
