'''
Death frame. Displayed briefly when the player dies
'''

import pygame

class DeathFrame:
    '''
    Displayed briefly on player death
    '''
    def __init__(self, game_engine):
        self.game_engine = game_engine

        self.width = self.game_engine.screen_width
        self.height = self.game_engine.screen_height

        # Flash a death frame briefly when the player dies
        self.flash_death_frame = False
        self.display_death_frame_for_count = int(self.game_engine.config.framerate / 8)
        self.death_frame_count = 0
        self.death_frame_color = (255, 0, 0) # Red
        self.death_frame = pygame.Surface([self.width, self.height])
        self.death_frame.fill(self.death_frame_color)
        self.death_frame.set_alpha(100) # Mostly see through
        self.death_frame = self.death_frame.convert() # For faster blitting
        self.rect = self.death_frame.get_rect()

    def flash(self):
        self.flash_death_frame = True

    def update(self):
        '''
        Update any values
        '''
        if self.flash_death_frame:
            if self.death_frame_count >= self.display_death_frame_for_count:
                self.flash_death_frame = False
                self.death_frame_count = 0
            else:
                self.death_frame_count += 1

    def draw(self, screen):
        '''
        Draw to the screen
        '''
        if self.flash_death_frame:
            screen.blit(self.death_frame, self.rect)