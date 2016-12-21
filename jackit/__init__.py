'''
The main game loop
'''

from deploy import SiteDeployment

class JackitGame:
    '''
    JackIt Game class
    '''

    @staticmethod
    def run():
        '''
        Run the game
        '''
        from jackit.core.engine import GameEngine

        while GameEngine.running:
            GameEngine.update()
