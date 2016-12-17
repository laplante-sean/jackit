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
        self.challenge_text = "CHALLENGE TEXT"

        # True if this block requires an adapter to unlock
        self.locked = False

    def is_locked(self):
        '''
        Getter for the locked instance variable
        '''
        return self.locked

    def interact(self):
        '''
        Called when an interactable block is interacted with
        '''

        # Start doing the code
        self.game_engine.code_editor.run(self.challenge_text)
        self.game_engine.current_level.player.invincible = True

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

        # Make it so player can die again
        self.game_engine.current_level.player.invincible = False
