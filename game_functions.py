import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Check the keydown events."""
    if event.key == pygame.K_RIGHT:
                # Move the ship to the right.
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
                # Move the ship to the left.
        ship.moving_left = True
    if event.key == pygame.K_UP:
        # Move the ship up.
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        # Move the ship down.
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        firing_bullets(ai_settings, screen, ship, bullets)


def firing_bullets(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reavched yet"""
    # Create a new bullet and add it to the bullet group.
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydup_events(event, ship):
    """Check the keydup events."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False



def check_events(ai_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keydup_events(event, ship)


def update_bullets(bullets):
    """Update position of billets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of the bullets.
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
            
def update_screen(ai_settings, screen, ship, bullets):
    """Update images on the screen and flip to the next screen"""
    # Redraw the screen during eqvh pass though the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Make the most revently drawn screen visible.
    pygame.display.flip()