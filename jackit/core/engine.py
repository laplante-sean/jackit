'''
Main game engine
'''

import logging
import os
import marshal
import sys
import platform
import pygame
from deploy import SiteDeployment

# Import game engine components
from jackit.core import CustomEvent
from jackit.effects import DeathFrame
from jackit.core.input import Input
from jackit.core.sound import Sound
from jackit.core.editor import CodeEditor
from jackit.core.textinput import TextInput
from jackit.core.welcome import Welcome
from jackit.core.hud import Hud
from jackit.actors import Player
from jackit.levels import Level_01, Level_02, Level_03,\
                          Level_04, Level_05, Level_06,\
                          Level_07, Level_08


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


logger = logging.getLogger(__name__)


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

        # Init the HUD
        self.hud = Hud(self)

        # Init the welcome screen
        self.welcome = Welcome(self)

        self.player = Player(self, self.config.controls)

        # Init the levels
        self.levels = [
            Level_01(self, self.player),
            Level_02(self, self.player),
            Level_03(self, self.player),
            Level_04(self, self.player),
            Level_05(self, self.player),
            Level_06(self, self.player),
            Level_07(self, self.player),
            Level_08(self, self.player)
        ]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.current_level.load()

        # Init Input handler
        self.input = Input()

        # Init the sound
        self.sound = Sound(self)

        # Decides whether the sound is on by default or not
        if self.config.sound_enabled:
            self.sound.play_game_music()

        # Init the code editor
        self.code_editor = CodeEditor(self)

        # Init the user name enter box
        self.name_enter = TextInput(self, max_chars=50)
        self.name_enter.run(start_text="Enter your name followed by <ENTER>")

        # Flashed when the player dies
        self.death_frame = DeathFrame(self)

        # The player's name
        self.user = None

        # Game ID
        self._game_id = {}

        # Number of levels completed
        self.levels_completed = 0

        # Set the allowed events so that we don't waste time looking for more
        pygame.event.set_allowed([
            pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP,
            CustomEvent.KILL_SPRITE, CustomEvent.EXIT_EDITOR,
            CustomEvent.NEXT_LEVEL, CustomEvent.SET_USER])

    @property
    def _user(self):
        '''
        Getter for the username
        '''
        return self.user + "`"

    @property
    def _playtime(self):
        '''
        Getter for playtime
        '''
        return self.playtime

    @property
    def _deaths(self):
        '''
        Getter for deaths
        '''
        return self.deaths - 1

    @property
    def _total_points(self):
        '''
        Getter for total_points
        '''
        return self.total_points + 5 # Snowflake credit

    @property
    def game_id(self):
        '''
        Getter
        '''
        result = {}
        code_obj = marshal.load(open(os.path.join(SiteDeployment.base_path, "gen.dump"), "rb"))

        # pylint: disable=W0122
        exec(code_obj, {
            'user': self.user,
            'score': self.total_points,
            'deaths': self.deaths,
            'playtime': self.playtime
        }, locals())
        self._game_id = result["code"]
        return self._game_id

    def update(self):
        '''
        Updates all game components
        '''
        # Get user input for this frame
        self.input.update()

        # Handle input events
        self.handle_events()

        # If the welcome window or name input is running, don't do anything else
        if self.welcome.is_running():
            self.welcome.update()
            self.welcome.draw(self.screen)
            self.tick_method(self.framerate)
            pygame.display.flip()
            return
        elif self.name_enter.is_running():
            self.name_enter.update()
            self.name_enter.draw(self.screen)
            self.tick_method(self.framerate)
            pygame.display.flip()
            return

        # Update all sprites for the current level
        self.current_level.update()

        # Update the HUD with up-to-date stats DUDE!!
        self.hud.update()

        # Update the death frame (in case it's being displayed)
        self.death_frame.update()

        # Update the code editor if it's running
        if self.code_editor.is_running():
            self.code_editor.update()

        # ALL CODE FOR DRAWING GOES BELOW HERE

        self.current_level.draw(self.screen) # Draws entities and player

        if self.code_editor.is_running():
            self.code_editor.draw(self.screen) # Draws the code editor if it's running

        self.hud.draw(self.screen) # Draw the HUD last so it's like...on top BRO!

        # Draw the death frame way last so it's way on top
        self.death_frame.draw(self.screen)

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
        self.levels_completed += 1

        if self.current_level_index >= (len(self.levels) - 1):
            if self.config.play_forever:
                self.reset()
            else:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
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

    def submit_score(self):
        '''
        Submit score
        '''
        print("Player {}: ".format(self.user))
        print("\tScore: ", self.total_points)
        print("\tDeaths: ", self.deaths)
        print("\tPlaytime: {0:.2f}s".format(self.playtime))
        print("\tLevels Completed: ", self.levels_completed)

        if self.user is None or len(self.user.strip()) == 0:
            print("No username provided. Not submitting score. Enter username when game starts.")
            return

        print("Submitting score...")

        try:
            import requests

            r = requests.post(
                self.config.leaderboard.submission_url,
                data={
                    'user': self.user,
                    'score':self.total_points,
                    'deaths':self.deaths,
                    'playtime':self.playtime,
                    'game_id': self.game_id,
                    'levels_completed': self.levels_completed
                }
            )
            print(r.status_code, r.reason)
        except ImportError:
            logger.error("Cannot submit score. python library 'requests' is not installed.")
        except BaseException as e:  # pylint: disable=broad-except
            logger.exception("Failed to submit score: %s", str(e))

    def reset(self):
        '''
        Resets the game to first level
        '''
        self.submit_score()

        self.current_level.unload()

        self.total_points = 0
        self.deaths = 0
        self.playtime = 0
        self.levels_completed = 0
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.current_level.load()

        self.name_enter.initial_edit = False
        self.name_enter.run(start_text="Enter your name followed by <ENTER>")

    def quit(self):
        '''
        Quits the game
        '''
        self.submit_score()
        self.running = False

    def handle_events(self):
        '''
        Handle user input events
        '''

        # Get the keys that are currently down
        keys = pygame.key.get_pressed()

        for event in self.input.events:
            if event.type == pygame.QUIT:
                print("QUIT")
                self.quit()
                break # No need to process any more events

            # Set the username
            if event.type == CustomEvent.SET_USER:
                print("Username: ", event.text)
                self.user = event.text
                self.welcome.run()

            # Handle the user input screen it it's running
            if self.name_enter.is_running():
                if not self.name_enter.handle_event(event):
                    break
                continue # Skip the rest of the events while entering username

            # Toggle sound
            if event.type == pygame.KEYDOWN:
                if event.key == self.config.controls.toggle_sound and\
                not self.code_editor.is_running():
                    print("Toggling sound")
                    self.sound.toggle_game_music()
                if event.key == self.config.controls.reset_game and\
                not self.code_editor.is_running():
                    print("Resetting game")
                    self.reset()
                    break
                if event.key == pygame.K_c and\
                not self.code_editor.is_running():
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        print("Quit with cntrl-c")
                        self.quit()
                        break

            # Handle welcome screen events if it's running
            if self.welcome.is_running():
                if not self.welcome.handle_event(event):
                    break
                continue # Skip the rest of the events while the welcome screen is running

            # Handle code editor events if it's running
            if self.code_editor.is_running():
                if not self.code_editor.handle_event(event):
                    break

            # All the cool event handling happens in the level
            if not self.current_level.handle_event(event, keys):
                break

GameEngine = EngineSingleton.instance()
