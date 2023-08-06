class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        self.screen_width = 1200
        self.screen_heigth = 700
        self.bg_color = (230,230,230)
        # Ship settings.
        self.ship_speed_factor = 0.8
        self.ship_limit = 2
        # Bullet settings.
        self.bullet_speed_factor = 3
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        # Alien settings.
        self.alien_speed_factor = 0.6
        self.fleet_drop_speed = 3
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        # How quickly the game speed up.
        self.game_speed_up = 1.1
        # Next level flag.
        self.next_level = -1
    
    def initialize_dynamic_settings(self):
        """Initialize settings that chage throughout the game."""
        self.ship_speed_factor = 0.8
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5
        # Scoring.
        self.alien_points = 50
    
    def increase_speed(self):
        """increase the speed whenever the player kill a fleet"""
        self.ship_speed_factor *= self.game_speed_up
        self.bullet_speed_factor *= self.game_speed_up
        self.alien_speed_factor *= self.game_speed_up
        self.alien_points = int(self.alien_points * self.game_speed_up)
    