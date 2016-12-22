'''
Code block entity
'''

import os
import re

from deploy import SiteDeployment
from jackit.core import BLOCK_WIDTH, BLOCK_HEIGHT
from jackit.core.animation import SpriteStripAnimation
from jackit.core.entity import Entity

class CodeBlock(Entity):
    '''
    Code block. Used to bring up the code view
    '''
    def __init__(self, game_engine, width, height, x_pos, y_pos):
        code_plug = os.path.join(SiteDeployment.resource_path, "sprites", "code_plug.bmp")

        animation = SpriteStripAnimation(
            code_plug, (0, 0, BLOCK_WIDTH, BLOCK_HEIGHT), 1, -1)

        super(CodeBlock, self).__init__(
            game_engine, width, height, x_pos, y_pos, animation=animation)

        if self.animation is None:
            self.image.fill((254, 68, 123))

        self.interactable = True
        self.collideable = False
        self._challenge_text = "CHALLENGE TEXT"
        self.original_text = None

        # True if this block requires an adapter to unlock
        self.locked = False

    @property
    def challenge_text(self):
        '''
        Getter for the instance variable _challenge_text
        '''
        return self._challenge_text

    @challenge_text.setter
    def challenge_text(self, value):
        self._challenge_text = value

        # When first populated, update the original_text
        if self.original_text is None:
            self.original_text = value

    def restore(self):
        '''
        Restore the orignal challenge text
        '''
        self.challenge_text = self.original_text

    def is_locked(self):
        '''
        Getter for the locked instance variable
        '''
        return self.locked

    def interact(self):
        '''
        Called when an interactable block is interacted with
        '''

        # Start the jackin_it animation
        self.game_engine.player.animation = self.game_engine.player.jackin_it.iter()
        self.game_engine.player.is_jackin_in = True
        self.game_engine.player.is_jackin_off = False

        self.game_engine.hud.display_hint("Press 'ESC' when you're done", 6)

        # Start doing the code
        self.game_engine.code_editor.run(self.challenge_text)
        self.game_engine.current_level.player.invincible = True

    def interaction_complete(self, event):
        '''
        Called when the interaction is complete
        '''

        # Start the jackin_off animation
        self.game_engine.player.animation = self.game_engine.player.jackin_off.iter()
        self.game_engine.player.is_jackin_in = False
        self.game_engine.player.is_jackin_off = True

        try:
            pattern = re.compile("import")
            if pattern.search(event.text) is not None:
                raise Exception("No Imports!")

            # Compile the code and catch any errors
            code_obj = compile(event.text, "<string>", "exec")

            self.game_engine.current_level.challenge_completed(code_obj)

            # Tell them how to clear the code changes they made
            self.game_engine.hud.display_hint("Clear code changes with 'Q'", 2)

            # Update the challenge text
            self.challenge_text = event.text
        except BaseException as e:
            self.game_engine.hud.display_popup("Your code blows! " + str(e), 7)

        # Make it so player can die again
        self.game_engine.current_level.player.invincible = False
