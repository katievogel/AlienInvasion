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

        #laser settings
        self.laser_speed = 2.0
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = (60, 60, 60)