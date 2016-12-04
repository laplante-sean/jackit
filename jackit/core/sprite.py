'''
Game sprite. Handles collision detection, sprite images, and animating the sprite
'''

import pygame

class Sprite(pygame.sprite.Sprite):
    '''
    Sprite in the game
    '''

    def __init__(self, color, width, height):
        super(Sprite, self).__init__()

        # Disable error in pylint. It doesn't like the Surface() call. Pylint is wrong.
        # pylint: disable=E1121
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.next_x = self.rect.x
        self.next_y = self.rect.y

    def prep_change_x(self, amount):
        '''
        Prepare to change the Y position of the rect
        '''
        self.next_x = self.rect.x + amount

    def prep_change_y(self, amount):
        '''
        Prepare to change the Y position of the rect
        '''
        self.next_y = self.rect.y + amount

    def commit_change(self):
        '''
        Actually change the X, Y position of the rect
        '''
        self.rect.x = self.next_x
        self.rect.y = self.next_y

    def getY(self):
        '''
        Getter for rect y position
        '''
        return self.rect.y

    def getX(self):
        '''
        Getter for rect x position
        '''
        return self.rect.x

    def getNextY(self):
        '''
        Getter for rect next y position
        '''
        return self.next_y

    def getNextX(self):
        '''
        Getter for rect next x position
        '''
        return self.next_x

    def get_collide_blocks(self, sprite_list):
        '''
        Get list of blocks this sprite is colliding with based on input list
        '''

        # Save the old values because they haven't been committed yet
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect.x = self.next_x
        self.rect.y = self.next_y

        # Check for collisions
        blocks = pygame.sprite.spritecollide(self, sprite_list, False)

        # Restore the values
        self.rect.x = old_x
        self.rect.y = old_y
        return blocks
