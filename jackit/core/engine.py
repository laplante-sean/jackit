'''
Main game engine
'''

import platform
import pygame
from deploy import SiteDeployment
from jackit.core import CustomEvent

# Import game engine components
from jackit.core.input import Input
from jackit.actors import Player
from jackit.core.patch import UserPatch
from jackit.core.editor import CodeEditor
from jackit.levels import Level_01, Level_02, Level_03,\
                          Level_04

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
        self.clock = pygame.time.Clock() # for framerate control
        self.running = True
        self.playtime = 0 # Current amout of time playing (seconds)

        if platform.system().lower() == "darwin":
            print("Detected MAC OS X. Run this app in low resolution mode on retina displays.")

        # Set the display mode
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

        # Init the levels
        self.levels = [Level_01(self), Level_02(self), Level_03(self), Level_04(self)]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.current_level.load()
        self.current_level.setup_level()

        # Init Input handler
        self.input = Input()

        # Init the code editor
        self.code_editor = CodeEditor(self)

        # Init the player
        self.player = Player(self, self.config.controls, spawn_point=self.current_level.spawn_point)

    def update(self):
        '''
        Updates all game components
        '''

        # Get user input for this frame
        self.input.update()

        # Handle input events
        self.handle_events()

        # Update all sprites for the current level
        self.current_level.update(self.player)

        # Update the code editor if it's running
        if self.code_editor.is_running():
            self.code_editor.update()

        # ALL CODE FOR DRAWING GOES BELOW HERE

        self.current_level.draw(self.screen, self.player) # Draws entities and player

        if self.code_editor.is_running():
            self.code_editor.draw(self.screen) # Draws the code editor if it's running

        # ALL CODE FOR DRAWING GOES ABOVE HERE

        # Maintain framerate
        milliseconds = self.clock.tick(self.framerate)
        self.playtime += milliseconds / 1000.0

        if self.config.is_development_mode():
            # Print framerate and playtime in titlebar.
            text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(self.clock.get_fps(), self.playtime)
            pygame.display.set_caption(text)

        # Update the screen with what has been drawn
        # TODO: Look into pygame.display.update() to update only things that have changed
        # Might improve perormance
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
            self.current_level.setup_level()
            self.player.rect.x = self.current_level.spawn_point[0]
            self.player.rect.y = self.current_level.spawn_point[1]

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

        # Handle code editor events if it's running
        if self.code_editor.is_running():
            self.code_editor.handle_events(self.input.events)

        # Get the keys that are currently down
        keys = pygame.key.get_pressed()

        for event in self.input.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == CustomEvent.KILL_ACTOR:
                print("Kill an actor. For now just respawn")
                event.actor.rect.x = self.current_level.spawn_point[0]
                event.actor.rect.y = self.current_level.spawn_point[1]
            elif event.type == CustomEvent.DESPAWN_ENTITY:
                print("Despawning entity")
            elif event.type == CustomEvent.EXIT_EDITOR:
                self.player.on_interactable_block.interaction_complete(event)
            elif event.type == CustomEvent.NEXT_LEVEL:
                self.next_level()

            # Don't process controller events for player when code editor is open
            if not self.code_editor.is_running():
                # Call to handle event for player
                self.player.handle_event(event, keys)

GameEngine = EngineSingleton.instance()
