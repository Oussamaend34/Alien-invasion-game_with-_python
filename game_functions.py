import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def get_number_aliens(ai_settings, alien_width):
    """Determine the number of the aliens in a fleet"""
    available_space_x = ai_settings.screen_width - (2*alien_width)
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_heigth, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = ai_settings.screen_heigth - 3 * alien_height - ship_heigth
    number_rows = available_space_y // (2 * alien_height)
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create one alien and add it to the group of aliens"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = int(alien.rect.height + 2 * alien.rect.height * row_number)
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, bullets, aliens):
    """Create a full fleet of aliens."""
    if len(aliens) == 0:
        bullets.empty()
        alien = Alien(ai_settings, screen)
        number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
        number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
        # Create the first line of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                create_alien(ai_settings, screen, aliens, alien_number, row_number) 

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):
    """Check the keydown events."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        # Move the ship to the left.
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        firing_bullets(ai_settings, screen, ship, bullets, stats)
    if event.key == pygame.K_q:
        sys.exit()


def firing_bullets(ai_settings, screen, ship, bullets, stats):
    """Fire a bullet if limit not reavched yet"""
    # Create a new bullet and add it to the bullet group.
    if len(bullets) < ai_settings.bullet_allowed and stats.game_stats:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydup_events(event,ai_settings, ship):
    """Check the keydup events."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, screen, sb, ship, aliens, bullets,stats, play_button, mouse_x, mouse_y):
    """Start a new game when the player press the button."""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_stats:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statics.
        stats.reset_stats()
        stats.game_stats = True
        sb.prep_score()
        sb.prep_ships()
        # Delete the aliens and the bullets.
        bullets.empty()
        aliens.empty()
        # Create a new fleet of aliens.
        create_fleet(ai_settings, screen, ship, bullets, aliens)
        ship.center_ship() 

def check_events(ai_settings, screen, sb, ship, aliens, bullets, stats, play_button):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, sb, ship, aliens, bullets, stats, play_button, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keydup_events(event,ai_settings, ship)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ship_left > 0:
        # Decrement ships_left
        stats.ship_left -= 1
        # Update scoreboard.
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        #create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, bullets, aliens)
        ship.center_ship
        # Pause.
        sleep(0.5)
    else:
        stats.game_stats = False
        pygame.mouse.set_visible(True)

def check_bottom_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship get hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of billets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of the bullets.
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen,stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > sb.high_score:
        sb.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen,stats, sb, ship, aliens, bullets):
    """Respnd to bullet and aliens that have collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        # Increase the level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, bullets, aliens)



def check_fleet_edges(ai_settings, aliens):
    """Respond approriatly if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and chande the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """check if the fleet is at an edge, and then update all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    for alien in aliens:
        if alien.rect.top >= ai_settings.screen_heigth:
            aliens.remove(alien)   
    # Check for ship aliens collision.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)        
    check_bottom_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
    

def update_screen(ai_settings, aliens, screen, stats, sb, ship, bullets, play_button):
    """Update images on the screen and flip to the next screen"""
    # Redraw the screen during eqvh pass though the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_stats:
        play_button.draw_botton()
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Make the most revently drawn screen visible.
    pygame.display.flip()