'''
Game sprite. Handles collision detection, sprite images, and animating the sprite
'''

import pygame

class GameSprite(pygame.sprite.Sprite):
    '''
    Sprite in the game
    '''

    def __init__(self, color, width, height):
        super(GameSprite, self).__init__()

        # Disable error in pylint. It doesn't like the Surface() call. It's wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def get_collide_blocks(self, sprite_list):
        '''
        Get list of blocks this sprite is colliding with based on input list
        '''
        return pygame.sprite.spritecollide(self, sprite_list, False)
