'''
Game camera
'''

import pygame

def simple_camera(screen_size, camera, target_rect):
    '''
    Simple camera implementation - Keeps target centered
    '''
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l + (screen_size[0] / 2), -t + (screen_size[1] / 2), w, h)

def complex_camera(screen_size, camera, target_rect):
    '''
    Complex camera implementation - Dynamic camera movement
    '''
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + (screen_size[0] / 2), -t + (screen_size[1] / 2), w, h

    l = min(0, l)                                   # stop scrolling at the left edge
    l = max(-(camera.width - screen_size[0]), l)    # stop scrolling at the right edge
    t = max(-(camera.height - screen_size[1]), t)   # stop scrolling at the bottom
    t = min(0, t)                                   # stop scrolling at the top
    return pygame.Rect(l, t, w, h)

class Camera:
    '''
    Game camera
    '''
    def __init__(self, screen_size, camera_func, level_width, level_height):
        self.screen_size = screen_size
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, level_width, level_height)

    def apply(self, target):
        '''
        Apply camera to target
        '''
        return target.rect.move(self.state.topleft)

    def update(self, target):
        '''
        Update camera state
        '''
        self.state = self.camera_func(self.screen_size, self.state, target.rect)
