import pygame
from pygame.sprite import Sprite
from settings import Settings

settings = Settings()
DEFAULT_IMAGE_SIZE = (settings.screen_width * .12, settings.screen_height * .2)
DEFAULT_LIVES_IMAGE_SIZE = (settings.screen_width * .12, settings.screen_height * .2)


class Ship(Sprite):
    '''
    A class to manage the ship
    '''
    def __init__(self, ai_game):
        '''
        Initialize the ship and set it starting position
        '''
        super().__init__()
        # pygame lets you treat all game elements as rectangles, or 'rects', for efficiency
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image 
        self.image = pygame.image.load('images/space-fighter-clipart-md.png')
 
        # Scale the image to appropriate size in play area
        self.scaled_image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        
        # Load ship position on screen
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)

        # movement flag: start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''
        Update ship's position based on the movement flag
        '''
        # update the ship's x value, not the rect. prevent from going off screen
        if self.moving_right and self.rect.right <self.screen_rect.right: 
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0: 
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        '''
        Re-center ship on the screen
        '''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def blitme(self):
        '''
        Draw the ship at its current location
        '''
        self.screen.blit(self.scaled_image, self.rect)

class ShipLivesGreen(Sprite):
    '''
    Class to control the graphical representation of how many lives are left for the player
    '''
    def __init__(self, ai_game):
        '''
        Initialize the ship and set it starting position
        '''
        super().__init__()
        # pygame lets you treat all game elements as rectangles, or 'rects', for efficiency
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship lives green image 
        self.image = pygame.image.load('images/green-circle.png')
 
        # Scale the image to appropriate size in play area
        self.scaled_image = pygame.transform.scale(self.image, DEFAULT_LIVES_IMAGE_SIZE)
        
        # Load ship lives images position on screen
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.scaled_image, self.rect)
        

class ShipLivesRed(Sprite):
    '''
    Class to control the graphical representation of how many lives are left for the player
    '''
    def __init__(self, ai_game):
        '''
        Initialize the ship and set it starting position
        '''
        super().__init__()
        # pygame lets you treat all game elements as rectangles, or 'rects', for efficiency
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship lives red image 
        self.image = pygame.image.load('images/red-x.png')
 
        # Scale the image to appropriate size in play area
        self.scaled_image = pygame.transform.scale(self.image, DEFAULT_LIVES_IMAGE_SIZE)
        
        # Load ship lives images position on screen
        self.rect = self.scaled_image.get_rect()                 

    def blitme(self):
        self.screen.blit(self.scaled_image, self.rect)