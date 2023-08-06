import pygame
from pygame.sprite import  Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and get rect.
        self.image = pygame.image.load('Images/alien_3.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Set it to start position.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the position of the alien in a decimal value.
        self.x = float(self.rect.x)

        # Moving flag.
        self.moving_flag = True

    def check_edges(self):
        """Return True if alien hit the edge of the screen."""
        if self.rect.right >= self.screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True

    def update(self):
        """Move the aliens right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship in its current location."""
        self.screen.blit(self.image, self.rect)
