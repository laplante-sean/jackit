'''
Code text editor
'''

import textwrap
from string import ascii_letters

import pygame

class CodeEditor:
    '''
    Code view text editor
    '''
    def __init__(self, game_engine):
        # Setup font stuff
        pygame.font.init()
        self.game_engine = game_engine
        self.config = self.game_engine.config.code_editor
        self.font = pygame.font.SysFont("Courier", self.config.font_size) # Courier for monospace

        self.running = False
        self.message = None
        self.render_msg_list = [] # Message broken into lines for rendering

        # Create a coding window slightly smaller than the main window
        self.width = self.game_engine.screen_width / 1.25
        self.height = self.game_engine.screen_height / 1.25

        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.code_window = pygame.Surface([self.width, self.height])
        self.code_window.fill(self.config.bg_color)
        self.code_window.set_alpha(self.config.bg_alpha)
        self.code_window = self.code_window.convert() # Convert the image for faster blitting
        self.rect = self.code_window.get_rect()

        # Put the code editor window in the center
        self.rect.x += (self.game_engine.screen_width - self.width) / 2
        self.rect.y += (self.game_engine.screen_height - self.height) / 2

        # Font rect. Moves down as lines are rendered
        self.font_rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)

        # The current position of the cursor
        self.cursor_position = 0
        self.cursor_line = 0
        self.cursor_pos_in_line = 0
        self.cursor_width = self.font.size(ascii_letters)[0] / len(ascii_letters)

        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.cursor = pygame.Surface([self.cursor_width, self.font.get_linesize()])
        self.cursor.fill(self.config.cursor_color)
        self.cursor.set_alpha(self.config.cursor_alpha)
        self.cursor = self.cursor.convert() # Convert the image for faster blitting
        self.cursor_rect = self.cursor.get_rect()

        # Start the cursor at the top left (0 position)
        self.cursor_rect.x = self.rect.x
        self.cursor_rect.y = self.rect.y

        # Calculate the maximum number of chars that will fit
        # Max chars must be an int so TextWrapper can wrap long words
        self.max_chars = int((
            self.width / (self.font.size(ascii_letters)[0] / len(ascii_letters))
        ) - 1)

        # Calculate the line size for the font
        self.line_size = self.font.get_linesize()
        self.textwrapper = textwrap.TextWrapper(
            width=self.max_chars,
            break_long_words=True,
            replace_whitespace=False,
            expand_tabs=False
        )

    def run(self, start_text="This is a single line of test text. Handle multiline later"):
        '''
        Setter for running instance variable
        '''
        self.running = True
        self.message = start_text

        # Set the key repeat values. Auto-triggers a KEYDOWN event while a key is held
        # after waiting an initial delay and then triggers subsequent KEYDOWN events
        # after an interval.
        pygame.key.set_repeat(self.config.key_repeat_delay, self.config.key_repeat_interval)

    def is_running(self):
        '''
        Getter for running instance variable
        '''
        return self.running

    def update(self):
        '''
        Update for code editor
        '''

        # Reset the Y position (moves down with each line in draw())
        self.font_rect.y = self.rect.y

        # Calc which line the cursor is on and where it is on the line
        self.cursor_line = 0
        self.cursor_pos_in_line = 0
        for i in range(self.cursor_position):
            if self.message[i] == "\n":
                self.cursor_line += 1
                self.cursor_pos_in_line = 0
            else:
                self.cursor_pos_in_line += 1

        # Break message into lines for rendering
        self.render_msg_list = []
        if self.message is not None and len(self.message):
            for line in self.message.split("\n"):
                if len(line) == 0:
                    self.render_msg_list.append(line)
                else:
                    for wrapped_line in self.textwrapper.wrap(line):
                        self.render_msg_list.append(wrapped_line)

    def render_line(self, screen, line):
        '''
        Render a line of text to the screen
        '''
        screen.blit(self.font.render(
            line,
            self.config.font_antialiasing,
            self.config.font_color
        ), self.font_rect)

        self.font_rect.y += self.line_size

    def draw(self, screen):
        '''
        Draw the code editor
        '''

        # Blit the background of the code window
        screen.blit(self.code_window, self.rect)

        # Render the lines onto the screen
        for line in self.render_msg_list:
            self.render_line(screen, line)


        # Handles case when there's only one character on the line
        if self.cursor_pos_in_line == len(self.render_msg_list[self.cursor_line]):
            self.cursor_pos_in_line = 0

        # Returns width and height, only need width
        w, _ = self.font.size(self.render_msg_list[self.cursor_line][:self.cursor_pos_in_line])
        self.cursor_rect.x = self.rect.x + w
        self.cursor_rect.y = self.rect.y + (self.cursor_line * self.line_size)

        #Draw the cursor
        screen.blit(self.cursor, self.cursor_rect)

    def k_delete(self):
        '''
        Handles the delete key
        '''
        if self.cursor_position == len(self.message):
            return

        self.message = ''.join((
            self.message[:self.cursor_position],
            self.message[self.cursor_position + 1:]
        ))

    def k_backspace(self):
        '''
        Handles the backspace key
        '''
        if self.cursor_position > 0:
            self.message = ''.join((
                self.message[:self.cursor_position - 1],
                self.message[self.cursor_position:]
            ))
            self.cursor_position -= 1

    def k_up(self):
        '''
        Handles the up arrow key
        '''
        if self.cursor_line == 0:
            return

        self.cursor_line -= 1
        if len(self.render_msg_list[self.cursor_line]) < self.cursor_pos_in_line:
            self.cursor_pos_in_line = len(self.render_msg_list[self.cursor_line])

    def k_down(self):
        '''
        Handles the down array key
        '''
        if self.cursor_line == len(self.render_msg_list) - 1:
            return

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
        if self.cursor_position < len(self.message):
            self.cursor_position += 1

    def k_tab(self):
        '''
        Handles the tab key
        '''
        self.message = ''.join((
            self.message[:self.cursor_position],
            " " * self.config.tab_size,
            self.message[self.cursor_position:]
        ))
        self.cursor_position += self.config.tab_size

    def k_return(self):
        '''
        Handles the enter key
        '''
        self.message = ''.join((
            self.message[:self.cursor_position],
            "\n",
            self.message[self.cursor_position:]
        ))
        self.cursor_position += 1

    def character_key(self, key):
        '''
        Handles the rest of the character keys
        '''
        if key < 32 or key > 126:
            return

        result = ""

        # Handle shift key being held
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            s = str(chr(key))
            result = s.upper()
        else:
            result = str(chr(key))

        self.message = ''.join((
            self.message[:self.cursor_position],
            result,
            self.message[self.cursor_position:]
        ))
        self.cursor_position += 1

    def handle_events(self, events):
        '''
        Handle input events while the code editor is up
        '''
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Quiting out of code editor")
                    self.running = False
                    self.message = None

                    # Undo the key repeat change so we don't effect the rest
                    # of the program
                    pygame.key.set_repeat() # Sets back to no repeat
                elif event.key == pygame.K_DELETE:
                    self.k_delete()
                elif event.key == pygame.K_LEFT:
                    self.k_left()
                elif event.key == pygame.K_RIGHT:
                    self.k_right()
                elif event.key == pygame.K_BACKSPACE:
                    self.k_backspace()
                elif event.key == pygame.K_TAB:
                    self.k_tab()
                elif event.key == pygame.K_RETURN:
                    self.k_return()
                else:
                    self.character_key(event.key)
