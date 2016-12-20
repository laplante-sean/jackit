'''
Implementation of pygame.sprite.Group() that
adds update_complete() call
'''

import pygame

class SpriteGroup(pygame.sprite.Group):
    '''
    Adds call for update_complete()
    '''
    def __init__(self):
        super(SpriteGroup, self).__init__()

    def update_complete(self):
        '''
        Calls update_complete for each sprite
        that has it
        '''
        for sprite in self.sprites():
            if hasattr(sprite, "update_complete"):
                sprite.update_complete()

    def set_attr(self, attr, value):
        '''
        Sets an attribute for each sprite
        that has it
        '''
        for sprite in self.sprites():
            if hasattr(sprite, attr):
                setattr(sprite, attr, value)

    def reset(self):
        '''
        Calls reset() for each sprite that has it
        '''
        for sprite in self.sprites():
            if hasattr(sprite, "reset"):
                sprite.reset()
