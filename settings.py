class Settings:
    '''
    A class to store all settings for Alien Invasion game
    '''
    def __init__(self):
        '''
        Initialize the game's settings
        '''
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 650
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Laser settings
        self.laser_speed = 2.5
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = (60, 60, 60)
        self.laser_max_num = 10

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 100
        # fleet direction of 1 represents right, -1 is left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speed_up_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''
        Initialize settings that will change throughout the game
        '''
        self.ship_speed = 1.5
        self.laser_speed = 2.5
        self.alien_speed = 1.0

        #fleet direct of 1 is right, -1 is left
        self.fleet_direction = 1

        #scoring settings
        self.alien_points = 50

    def increase_speed(self):
        '''
        Increases the various speed settings
        '''
        self.ship_speed *= self.speed_up_scale
        self.laser_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
