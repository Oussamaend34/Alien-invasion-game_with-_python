import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

ai_settings = Settings()

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_heigth))
    pygame.display.set_caption("Alien Invasion")

    # Make an instance to store game statics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make the ship.
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets.
    bullets = Group()

    # Make a group to store aliens.
    aliens = Group()

    # Make a play botton.
    play_button = Button(ai_settings, screen, "Play")
    
    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, bullets, aliens) 

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, sb, ship, aliens, bullets, stats, play_button)
        
        if stats.game_stats:
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets )
        gf.update_screen(ai_settings, aliens, screen, stats, sb, ship, bullets, play_button)

run_game()
