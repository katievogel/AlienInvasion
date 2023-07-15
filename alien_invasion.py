import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
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

        # An instance of GameStats to store game statistics. A good example showing that an instance of a class represents state an object
        self.stats = GameStats(self)

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

        # start game in an inactive state
        self.game_active = False

        # make the play button
        self.play_button = Button(self, "Play")

    def _create_alien(self, x_position, y_position):
        '''
        Create an alien and place it in a row
        '''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _create_fleet(self):
        '''
        Create the fleet of aliens
        '''
        # Make one alien, and add until there is no room
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row - reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _change_fleet_direction(self):
        '''
        Drop down the entire fleet  and change direction of movement
        '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_fleet_edges(self):
        '''
        Respond appropriately if any aliens have reached the edge the screen/play area
        '''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

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
        self._check_laser_alien_collisions()
        
    def _check_laser_alien_collisions(self):
        '''
        Respond to laser-alien collisions. Remove any lasers & aliens that have collided
        '''    
        collisions = pygame.sprite.groupcollide(
            self.lasers, self.aliens, True, True
        )
        if not self.aliens:
            # destroy existing lasers and make new fleet
            self.lasers.empty()
            self._create_fleet()
    
    def _ship_hits(self):
        '''
        Respond to the ship being his by an alien
        '''
        if self.stats.ships_left > 0:
            # Decrement ships left on each hit
            self.stats.ships_left = -1

            # Get rid of any remaining lasers and aliens on hit
            self.lasers.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship for the next round
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause for player to get ready for next round
            sleep(0.5)
        
        else:
            self.game_active = False

    def _check_for_aliens_at_bottom(self):
        '''
        Check if any aliens have reached the bottom of the screen
        '''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # treat this the same way as if the ship was hit by an alien - a losing condition
                self._ship_hits()
                break
    
    def _update_aliens(self):
        '''
        Check if fleet is at the edge, update the positions of all aliens in the fleet.
        '''
        self._check_fleet_edges()
        self.aliens.update()

        # check for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hits()

        # check for aliens hitting the bottom of screen
        self._check_for_aliens_at_bottom()
    
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

    def _check_play_button(self, mouse_position):
        '''
        Start a new game when the player clicks 'Play'. Prevent game from resetting if button area is clicked when the button is not visible
        '''
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked and not self.game_active:
            #reset game stats whenever Play is clicked
            self.stats.reset_stats()
            self.lasers.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.game_active = True

    def _check_events(self):
        # watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)

    def _update_screen(self):
        # redraw the screeen during each pass of the loop
        self.screen.fill(self.settings.bg_color)
        for laser in self.lasers.sprites():
            laser.draw_laser()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # make the most recently drawn screen visible
        pygame.display.flip()
    
    def run_game(self):
        '''
        Start the main loop for the game
        '''
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_laser()
                self._update_aliens()
            
            self._update_screen()
            # setting the frame rate. will try to loop 60x/s
            self.clock.tick(60)

if __name__ == '__main__':
    # make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()