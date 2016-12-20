'''
Main game engine
'''

import sys
import platform
import pygame
from deploy import SiteDeployment

# Import game engine components
from jackit.core import CustomEvent
from jackit.core.input import Input
from jackit.core.sound import Sound
from jackit.core.editor import CodeEditor
from jackit.core.welcome import Welcome
from jackit.core.hud import Hud
from jackit.actors import Player
from jackit.levels import Level_01, Level_02, Level_03,\
                          Level_04, Level_05, Level_06

MAC_OSX_10_12_2_NOTE = """Because of a bug in pygame, this game is
currently not working on Mac OS X 10.12.2. 
Please install pygame_sdl2 and re-run game.py 
with the '--sdl2' argument to fix this issue

pygame_sdl2 can be found here: 
https://github.com/renpy/pygame_sdl2

To setup, brew is required. If you don't have it, get it like this:
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Then do this to install pygame_sdl2:
$ git clone https://github.com/renpy/pygame_sdl2
$ cd pygame_sdl2
$ brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_ttf
$ pip install cython
$ python3 setup.py install

Then finally, from the jackit repo:
$ python3 game.py --sdl2"""

class EngineSingleton:
    '''
    Main game engine. Handles updating game componenents
    '''
    _instance = None

    @classmethod
    def instance(cls):
        '''
        Get instance of EngineSingleton
        '''
        if cls._instance is None:
            cls._instance = EngineSingleton()
            return cls._instance
        return cls._instance

    def __init__(self):
        pygame.init()

        self.config = SiteDeployment.config
        self.screen_width = self.config.width
        self.screen_height = self.config.height
        self.screen_size = (self.config.width, self.config.height)
        self.fullscreen = self.config.fullscreen
        self.framerate = self.config.framerate
        self.running = True

        # Current amout of time playing (seconds)
        self.playtime = 0

        # Total points
        self.total_points = 0

        # Number of deaths (factors into final score)
        self.deaths = 0

        self.clock = pygame.time.Clock() # for framerate control
        if self.config.accurate_framerate:
            # More accurate but uses more CPU and therefore more power
            self.tick_method = self.clock.tick_busy_loop
        else:
            self.tick_method = self.clock.tick

        if platform.system().lower() == "darwin":
            if platform.mac_ver()[0] == "10.12.2" and pygame.get_sdl_version()[0] < 2:
                print(MAC_OSX_10_12_2_NOTE)
                sys.exit(-1)

            print("Detected MAC OS X. Run this app in low resolution mode on retina displays.")


        # Set the display mode
        if self.fullscreen:
            # Run with all the fancy when doing fullscreen
            self.screen = pygame.display.set_mode(
                self.screen_size,
                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

        self.player = Player(self, self.config.controls)

        # Init the levels
        self.levels = [
            Level_01(self, self.player),
            Level_02(self, self.player),
            Level_03(self, self.player),
            Level_04(self, self.player),
            Level_05(self, self.player),
            Level_06(self, self.player)
        ]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.current_level.load()

        # Init Input handler
        self.input = Input()

        # Init the sound
        self.sound = Sound(self)
        self.sound.play_game_music()

        # Init the code editor
        self.code_editor = CodeEditor(self)

        # Init the HUD
        self.hud = Hud(self)

        # Init the welcome screen
        self.welcome = Welcome(self)
        self.welcome.run()

        # Set the allowed events so that we don't waste time looking for more
        pygame.event.set_allowed([
            pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP,
            CustomEvent.KILL_SPRITE, CustomEvent.EXIT_EDITOR,
            CustomEvent.NEXT_LEVEL])

    def update(self):
        '''
        Updates all game components
        '''
        # Get user input for this frame
        self.input.update()

        # Handle input events
        self.handle_events()

        # If the welcome window is running, don't do anything else
        if self.welcome.is_running():
            self.welcome.update()
            self.welcome.draw(self.screen)
            pygame.display.flip()
            return

        # Update all sprites for the current level
        self.current_level.update()

        # Update the HUD with up-to-date stats DUDE!!
        self.hud.update()

        # Update the code editor if it's running
        if self.code_editor.is_running():
            self.code_editor.update()

        # ALL CODE FOR DRAWING GOES BELOW HERE

        self.current_level.draw(self.screen) # Draws entities and player

        if self.code_editor.is_running():
            self.code_editor.draw(self.screen) # Draws the code editor if it's running

        self.hud.draw(self.screen) # Draw the HUD last so it's like...on top BRO!

        # ALL CODE FOR DRAWING GOES ABOVE HERE

        # Maintain framerate
        milliseconds = self.tick_method(self.framerate)
        self.playtime += milliseconds / 1000.0

        if self.config.is_development_mode():
            # Print framerate and playtime in titlebar.
            text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(self.clock.get_fps(), self.playtime)
            pygame.display.set_caption(text)

        # Update the screen with what has been drawn
        pygame.display.flip()

    def next_level(self):
        '''
        Move to the next level
        '''
        if self.current_level_index >= (len(self.levels) - 1):
            self.running = False
        else:
            self.current_level.unload()
            self.current_level_index += 1
            self.current_level = self.levels[self.current_level_index]
            self.current_level.load()

    def is_rect_in_death_zone(self, rect):
        '''
        Is the provided rect in the current level's death zone
        '''
        top, left, width, height = self.current_level.death_zone
        if not (left <= rect.x and rect.x <= width):
            return True
        elif not (top <= rect.y and rect.y <= height):
            return True
        return False

    def handle_events(self):
        '''
        Handle user input events
        '''

        # Get the keys that are currently down
        keys = pygame.key.get_pressed()

        for event in self.input.events:
            if event.type == pygame.QUIT:
                self.running = False
                break # No need to process any more events

            # Handle global events
            if event.type == pygame.KEYDOWN:
                if event.key == self.config.controls.toggle_sound and not self.code_editor.is_running():
                    print("Toggling sound")
                    self.sound.toggle_game_music()

            # Handle welcome screen events if it's running
            if self.welcome.is_running():
                if not self.welcome.handle_event(event):
                    break
                continue # Skip the rest of the events while the welcome screen is running

            # Handle code editor events if it's running
            if self.code_editor.is_running():
                if not self.code_editor.handle_event(event):
                    break
            
            if not self.current_level.handle_event(event, keys):
                break

GameEngine = EngineSingleton.instance()
