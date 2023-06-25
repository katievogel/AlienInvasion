import sys

import pygame

from settings import Settings
from ship import Ship
from laser import Laser
from alien import Alien

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

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self) #self gives Ship access to AlienInvasion resources via AlienInvasion instance
        self.lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # setting the background color
        self.bg_color = (230, 230, 230)

    def _create_fleet(self):
        '''
        Create the fleet of aliens
        '''
        # Make one alien, and add
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width
    
    def _fire_laser(self):
        '''
        Create a new laser and add it to the lasers group
        '''
        if len(self.lasers) < self.settings.laser_max_num:
            new_laser = Laser(self)
            self.lasers.add(new_laser)

    def _update_laser(self):
        '''
        Update position of lasers and get rid of old ones
        '''
        self.lasers.update()
         # get rid of lasers that passed the screen for memory management
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

    def _check_keydown_event(self, event):
        '''
        Respond to key presses
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_laser()

    def _check_keyup_event(self, event):
        '''
        Respond to key releases
        '''
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _check_events(self):
        # watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _update_screen(self):
        # redraw the screeen during each pass of the loop
        self.screen.fill(self.settings.bg_color)
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # make the most recently drawn screen visible
        pygame.display.flip()
    
    def run_game(self):
        '''
        Start the main loop for the game
        '''
        while True:
            self._check_events()
            self.ship.update()
            self._update_laser()
            self._update_screen()
                
            # setting the frame rate. will try to loop 60x/s
            self.clock.tick(60)

if __name__ == '__main__':
    # make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()