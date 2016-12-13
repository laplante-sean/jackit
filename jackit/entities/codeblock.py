'''
Code block entity
'''

import re
import pygame

from jackit.core.entity import Entity

class CodeBlock(Entity):
    '''
    Code block. Used to bring up the code view
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        super(CodeBlock, self).__init__(game_engine, width, height, x_pos, y_pos)
        self.image.fill((254, 68, 123))
        self.interactable = True
        self.collideable = False
        self.interaction_guard = pygame.sprite.Group()
        self.challenge_text = "CHALLENGE TEXT"

    def collide(self, actor):
        actor.on_interactable_block = self

    def interact(self):
        '''
        Called when an interactable block is interacted with
        '''

        # Guard rects to the left, right, and above the interactable object
        self.interaction_guard.add(
            self.game_engine.current_level.create_platform(
                (self.rect.left - self.game_engine.current_level.level_map_block_x),
                (self.rect.top)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.left - self.game_engine.current_level.level_map_block_x),
                (self.rect.top - self.game_engine.current_level.level_map_block_y)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.right),
                (self.rect.top)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.right),
                (self.rect.top - self.game_engine.current_level.level_map_block_y)
            ),
            self.game_engine.current_level.create_platform(
                (self.rect.left),
                (self.rect.top - self.game_engine.current_level.level_map_block_y)
            )
        )

        self.game_engine.current_level.entities.add(self.interaction_guard)

        # Start doing the code
        self.game_engine.code_editor.run(self.challenge_text)

    def interaction_complete(self, event):
        '''
        Called when the interaction is complete
        '''
        try:
            # TODO: More security
            pattern = re.compile(r'.*import.*')
            if pattern.match(event.text) is not None:
                raise Exception("No Imports!")

            # Compile the code and catch any errors
            code_obj = compile(event.text, "<string>", "exec")

            self.game_engine.current_level.challenge_completed(code_obj)

            # Update the challenge text
            self.challenge_text = event.text
        except BaseException as e:
            print("Your code blows! ", str(e))

        # Remove the interaction guard from around the object
        self.game_engine.current_level.entities.remove(self.interaction_guard)

        # TODO: Create a sprite.Group of sprites to clear from the screen.
        # Make it part of the Level base class. In Level update, clear the list
        self.interaction_guard.clear(self.game_engine.screen, (0, 0, 255))
