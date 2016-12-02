'''
User controllable player
'''

from jackit.core import EngineComponent
from jackit.core.sprite import GameSprite

class Player(EngineComponent):
    '''
    User controlled player
    '''

    def __init__(self, game_engine):
        super(Player, self).__init__(game_engine)
        self.sprite = GameSprite((255, 0, 0), 40, 60)
        self.game_engine.active_sprite_list.add(self.sprite)

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None

    def update(self):
        '''
        Move the player
        '''

        # Gravity
        self.calc_grav()

        # Move left/right
        self.sprite.rect.x += self.change_x

        '''
        # See if we hit anything
        block_hit_list = self.sprite.get_collide_blocks(self.level.platform_list)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.sprite.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.sprite.rect.left = block.rect.right
        '''

        # Move up/down
        self.sprite.rect.y += self.change_y

        '''
        # Check and see if we hit anything
        block_hit_list = self.sprite.get_collide_blocks(self.level.platform_list)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.sprite.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.sprite.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0
        '''

    def calc_grav(self):
        '''
        Calculate gravity
        '''
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        ground = self.game_engine.screen_height - self.sprite.rect.height
        if self.sprite.rect.y >= ground and self.change_y >= 0:
            self.change_y = 0
            self.sprite.rect.y = ground

    def jump(self):
        '''
        Called when the user hits the jump button. Makes the character jump
        '''

        # If we're on the ground, it's OK to jump
        if self.sprite.rect.bottom >= self.game_engine.screen_height:
            self.change_y = -10
        else:
            # TODO: Check if we're on a platform
            # Move down 2 pixels (doesn't work well with 1)
            self.sprite.rect.y += 2
            platform_hit_list = self.sprite.get_collide_blocks([])
            self.sprite.rect.y -= 2 # Reset position after check

            if len(platform_hit_list) > 0:
                self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        '''
        Called when the user hits the left button. Moves the character left
        '''
        self.change_x = -6

    def go_right(self):
        '''
        Called when the user hits the right button. Moves the character right
        '''
        self.change_x = 6

    def stop(self):
        '''
        Stops the characters movement when the user releases the keys
        '''
        self.change_x = 0
