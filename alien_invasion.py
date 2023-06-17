import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    '''
    Overall class to manage game assets and behavior
    '''

    def __init__(self):
        '''
        Initialize the game, and create game resources
        '''
        pygame.init()

        # using Clock for frame rate control
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self) #self gives Ship access to AlienInvasion resources via AlienInvasion instance


        # setting the background color
        self.bg_color = (230, 230, 230)

    def _check_events(self):
        # watch for keyboard and mouse events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def _update_screen(self):
        # redraw the screeen during each pass of the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # make the most recently drawn screen visible
        pygame.display.flip()
    
    def run_game(self):
        '''
        Start the main loop for the game
        '''
        while True:
            self._check_events()
            self._update_screen()
                
            # setting the frame rate. will try to loop 60x/s
            self.clock.tick(60)

if __name__ == '__main__':
    # make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()