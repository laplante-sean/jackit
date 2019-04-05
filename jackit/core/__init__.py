'''
Global declaration of custom event so everyone has access
'''

import pygame

class CustomEvent:
    '''
    Custom event mapping
    '''
    KILL_SPRITE = pygame.USEREVENT + 0
    EXIT_EDITOR = pygame.USEREVENT + 2
    NEXT_LEVEL = pygame.USEREVENT + 3
    SET_USER = pygame.USEREVENT + 4


# Global values for block size
BLOCK_WIDTH = 24
BLOCK_HEIGHT = 24


def game_code(user, total_points, deaths, playtime):
    '''
    Do the things
    '''
    import os
    import marshal
    from deploy import SiteDeployment

    result = {}
    code_obj = marshal.load(open(os.path.join(SiteDeployment.base_path, "gen.dump"), "rb"))

    # pylint: disable=W0122
    exec(code_obj, {
        'user': user,
        'score': total_points,
        'deaths': deaths,
        'playtime': playtime
    }, locals())

    return result["code"]
