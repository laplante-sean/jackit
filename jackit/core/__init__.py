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


def submit(url, user, total_points, deaths, playtime, levels_completed):
    '''
    Do the things
    '''
    import os
    import marshal
    from deploy import SiteDeployment

    code_obj = marshal.load(open(os.path.join(SiteDeployment.base_path, "gen.dump"), "rb"))

    # pylint: disable=W0122
    exec(code_obj, {
        'submission_url': url,
        'user': user,
        'score': total_points,
        'deaths': deaths,
        'playtime': playtime,
        'levels_completed': levels_completed
    }, locals())


def submitlvl(url, user, total_points, deaths, playtime, levels_completed, level_completed, completed_level):
    '''
    Do more things
    '''
    import os
    import marshal
    from deploy import SiteDeployment

    result = {}

    code_obj = marshal.load(open(os.path.join(SiteDeployment.base_path, "gen2.dump"), "rb"))

    # pylint: disable=W0122
    exec(code_obj, {
        'submission_url': url,
        'user': user,
        'score': total_points,
        'deaths': deaths,
        'playtime': playtime,
        'levels_completed': levels_completed,
        'level_completed': level_completed,
        'completed_level': completed_level
    }, locals())
