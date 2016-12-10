'''
Code text editor
'''

import textwrap
from string import ascii_letters

import pygame

from jackit.core import CustomEvent

# Map of special keys to their values when the
# shift key is being held
KEY_TO_SHIFT_MAP = {
    '`':'~',
    '1':'!',
    '2':'@',
    '3':'#',
    '4':'$',
    '5':'%',
    '6':'^',
    '7':'&',
    '8':'*',
    '9':'(',
    '0':')',
    '-':'_',
    '=':'+',
    '[':'{',
    ']':'}',
    '\\':'|',
    ';':':',
    "'":'"',
    ',':'<',
    '.':'>',
    '/':'?'
}

class CodeEditor:
    '''
    Code view text editor
    '''
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.config = self.game_engine.config.code_editor
        self.running = False
        self.text = None

        # Init the font
        pygame.font.init()
        self.font = pygame.font.SysFont("Courier", self.config.font_size) # Courier for monospace

        # Lines to render in the text view
        self.render_text_list = []

        # Create a coding window slightly smaller than the main window
        self.width = self.game_engine.screen_width / 1.25
        self.height = self.game_engine.screen_height / 1.25
        self.code_window = pygame.Surface([self.width, self.height])
        self.code_window.fill(self.config.bg_color)
        self.code_window.set_alpha(self.config.bg_alpha)
        self.code_window = self.code_window.convert() # Convert the image for faster blitting
        self.rect = self.code_window.get_rect()

        # Put the code editor window in the center
        self.rect.x += (self.game_engine.screen_width - self.width) / 2
        self.rect.y += (self.game_engine.screen_height - self.height) / 2

        # Text rect, moves down as lines are rendered
        self.text_rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)

        # Setup the cursor
        self.cursor_position = 0
        self.cursor_line = 0
        self.cursor_pos_in_line = 0
        self.cursor_width = self.font.size(ascii_letters)[0] / len(ascii_letters)
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
        self.max_chars = int(
            (self.width / (self.font.size(ascii_letters)[0] / len(ascii_letters))) - 1
        ) - 1

        # Calculate the line size for the font
        self.line_size = self.font.get_linesize()

        # Create the text wrapper
        self.textwrapper = textwrap.TextWrapper(
            width=self.max_chars,
            break_long_words=True,
            replace_whitespace=False,
            expand_tabs=False,
            drop_whitespace=True
        )

    def run(self, start_text="This is one line\nThis is another line\n\nBlank plus another."):
        '''
        Setter for running instance variable. Sets the window text as well
        '''
        self.running = True
        self.text = start_text
        self.cursor_position = 0
        self.cursor_line = 0
        self.cursor_pos_in_line = 0

        # Set the key repeat values. Auto-triggers a KEYDOWN event while a key is held
        # after waiting an initial delay and then triggers subsequent KEYDOWN events
        # after an interval.
        pygame.key.set_repeat(self.config.key_repeat_delay, self.config.key_repeat_interval)

    def stop(self):
        '''
        Called when the user hits the escape key
        '''
        self.running = False

        # Trigger an event and send off the user edited text
        pygame.event.post(pygame.event.Event(CustomEvent.EXIT_EDITOR, {"text": self.text}))

        # Undo the key repeat change so we don't effect the rest
        # of the program
        pygame.key.set_repeat() # Sets back to no repeat

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
        self.text_rect.y = self.rect.y

        # Build the list of strings to render
        self.build_render_text_list()

        # Get cursor render position
        self.cursor_line, self.cursor_pos_in_line = self.get_cursor_line_and_position()

    def build_render_text_list(self):
        '''
        Build the list of strings to render
        '''
        # Break message into lines for rendering
        self.render_text_list = []
        if self.text is not None and len(self.text):
            for line in self.text.split("\n"):
                if len(line) == 0:
                    self.render_text_list.append(line)
                else:
                    self.render_text_list.extend(self.textwrapper.wrap(line))

            self.text = '\n'.join(self.render_text_list) # Re-write text with the broken up lines

    def get_cursor_line_and_position(self):
        '''
        Calc which line the cursor is on and where it is on the line
        '''
        line = 0
        position_in_line = 0
        for i in range(self.cursor_position):
            if self.text[i] == "\n":
                line += 1
                position_in_line = 0
            else:
                position_in_line += 1

        return line, position_in_line

    def get_cursor_pos(self, line, position_in_line):
        '''
        Calc where the cursor would be in self.text at the given
        line and position in that line
        '''
        cur_line = 0
        cur_pos = 0
        real_pos = 0
        for i in range(len(self.text)):
            if cur_line == line and cur_pos == position_in_line:
                break

            if self.text[i] == "\n":
                cur_line += 1
                cur_pos = 0
            else:
                cur_pos += 1
            real_pos += 1

        return real_pos

    def render_line(self, screen, line):
        '''
        Render a line of text to the screen
        '''
        screen.blit(self.font.render(
            line,
            self.config.font_antialiasing,
            self.config.font_color
        ), self.text_rect)

        self.text_rect.y += self.line_size

    def draw(self, screen):
        '''
        Draw the code editor
        '''

        # Blit the background of the code window
        screen.blit(self.code_window, self.rect)

        # When everything is deleted there is nothing to do here
        if len(self.render_text_list):
            # Returns width and height, only need width to set cursor position
            w, _ = self.font.size(self.render_text_list[self.cursor_line][:self.cursor_pos_in_line])
            self.cursor_rect.x = self.rect.x + w
            self.cursor_rect.y = self.rect.y + (self.cursor_line * self.line_size)
        else:
            # Reset the cursor
            self.cursor_rect.x = self.rect.x
            self.cursor_rect.y = self.rect.y

        '''
        # Check if we can fit all the text on the screen
        if (len(self.render_text_list) * self.line_size) >= self.height:
            # How many lines fit under the cursor?
            under_lines = int((self.rect.bottom - self.cursor_rect.y)/ self.line_size)
            over_lines = int((self.cursor_rect.y - self.rect.top) / self.line_size)

            #if under_lines == 0:


            self.render_text_list = self.render_text_list[
                (self.cursor_line - over_lines):(self.cursor_line + under_lines)
            ]
        '''

        # Render the lines onto the screen
        for line in self.render_text_list:
            self.render_line(screen, line)

        #Draw the cursor
        screen.blit(self.cursor, self.cursor_rect)

    def handle_events(self, events):
        '''
        Handle input events while the code editor is up
        '''
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()
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
                elif event.key == pygame.K_UP:
                    self.k_up()
                elif event.key == pygame.K_DOWN:
                    self.k_down()
                else:
                    self.character_key(event.key)

    def k_delete(self):
        '''
        Handles the delete key
        '''
        if self.cursor_position == len(self.text):
            return

        self.text = ''.join((
            self.text[:self.cursor_position],
            self.text[self.cursor_position + 1:]
        ))

    def k_backspace(self):
        '''
        Handles the backspace key
        '''
        if self.cursor_position > 0 and self.cursor_position <= len(self.text):
            self.text = ''.join((
                self.text[:self.cursor_position - 1],
                self.text[self.cursor_position:]
            ))
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
        if self.cursor_position < len(self.text):
            self.cursor_position += 1

    def k_tab(self):
        '''
        Handles the tab key
        '''
        self.text = ''.join((
            self.text[:self.cursor_position],
            " " * self.config.tab_size,
            self.text[self.cursor_position:]
        ))
        self.cursor_position += self.config.tab_size

    def k_return(self):
        '''
        Handles the enter key
        '''
        self.text = ''.join((
            self.text[:self.cursor_position],
            "\n",
            self.text[self.cursor_position:]
        ))
        self.cursor_position += 1

    def character_key(self, key):
        '''
        Handles the rest of the keys
        '''

        if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            return # Skip the event for the shift key itself

        # Handle shift key
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            if key >= 97 and key <= 122:
                key = ord(chr(key).upper())
            else:
                if KEY_TO_SHIFT_MAP.get(chr(key), None) is not None:
                    key = ord(KEY_TO_SHIFT_MAP[chr(key)])

        self.text = ''.join((
            self.text[:self.cursor_position],
            chr(key),
            self.text[self.cursor_position:]
        ))
        self.cursor_position += 1

    def k_up(self):
        '''
        Handles the up arrow key
        '''
        if self.cursor_line == 0:
            return

        # This should never happen b/c we should be on line 0 if the
        # render_msg_list is empty. Check anyway to prevent potential
        # index out of bounds below
        if len(self.render_text_list) == 0:
            return

        self.cursor_line -= 1
        if len(self.render_text_list[self.cursor_line]) < self.cursor_pos_in_line:
            self.cursor_pos_in_line = len(self.render_text_list[self.cursor_line])

        # Determine where we are in the actual text
        self.cursor_position = self.get_cursor_pos(self.cursor_line, self.cursor_pos_in_line)

    def k_down(self):
        '''
        Handles the down array key
        '''
        if len(self.render_text_list) == 0:
            return

        if self.cursor_line == len(self.render_text_list) - 1:
            return

        self.cursor_line += 1
        if len(self.render_text_list[self.cursor_line]) < self.cursor_pos_in_line:
            self.cursor_pos_in_line = len(self.render_text_list[self.cursor_line])

        # Determine where we are in the actual text
        self.cursor_position = self.get_cursor_pos(self.cursor_line, self.cursor_pos_in_line)
