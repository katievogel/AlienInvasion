import pygame
from pygame.sprite import Sprite

class PewPew(Sprite):
    '''
    A class to manage lasers fired from the ship
    '''
    def __init__(self, ai_game):
        '''
        Create a laser object at the ship's current position
        '''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.pewpew_color

        # create a laser rect at 0,0 and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.pewpew.width, self.settings.pewpew.height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # store the laser's position as a float
        self.y = float(self.rect.y)