import pygame

class Ship():
    def __init__(self, ai_settings, screen):
        """Initialize the ship and sets its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('Images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store the center of the ship.
        self.center = float(self.rect.centerx)
        self.flying = float(self.rect.centery)

        # Moving flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def update(self):
        """Updates the ship's mouvement based on the mouving flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.flying -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.flying += self.ai_settings.ship_speed_factor
        self.rect.centerx = int(self.center)
        self.rect.centery = int(self.flying)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
