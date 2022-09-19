import sys

from time import sleep

import pygame

import random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from superbullet import Superbullet
from alien import Alien
from lazer import Lazer
from star import Star
from explosion import Explosion

FPS = 60


class AlienInvasion:
    """Class to manage resources and game behaviour"""

    def __init__(self):
        """Initialising game and game resources"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion!")

        self.clock = pygame.time.Clock()

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self, 3)
        self.bullets = pygame.sprite.Group()
        self.superbullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.lazers = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self._create_starry_sky()

        self.play_button = Button(self, "play")
        self.sound_button = Button(self, "sound")

    def run_game(self):
        """Lauching main cycle of the game"""
        while True:
            self._check_events()
            self.clock.tick(FPS)

            if self.stats.game_active:
                self.ship.update()
                self._update_ship_health()
                self._update_bullets()
                self._update_superbullets()
                self._shoot_lazers()
                self._check_lazer_position()
                self._update_explosions()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # Checking IO events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)

    def _check_button(self, mouse_pos):
        """Checking if any of the buttons was pressed"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        sound_button_clicked = self.sound_button.rect.collidepoint(mouse_pos)

        # Launching game if Play button is pressed
        if play_button_clicked and not self.stats.game_active:
            self._game_launch()
            if self.settings.sound_on:
                self.settings.play_sound_effect("press_button")

        # Muting
        elif sound_button_clicked and self.settings.sound_on:
            self.settings.play_sound_effect("press_button")

            # Changing image from mute to sound on
            # As the next click on this button is to turn the sound on
            sound_on_image = pygame.image.load("images/sound_on_button.png")
            self.sound_button.image.blit(sound_on_image, [0, 0])
            self.settings.sound_on = False

        # Turning the sound on if on mute
        elif sound_button_clicked and not self.settings.sound_on:
            self.settings.play_sound_effect("press_button")

            # Changing image from sound on to mute
            # As the next click on this button is to mute
            mute_image = pygame.image.load("images/mute_button.png")
            self.sound_button.image.blit(mute_image, [0, 0])
            self.settings.sound_on = True

    def _game_launch(self):
        # Resetting game statistics
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

        # Resetting alien and (super)bullets lists
        self.aliens.empty()
        self.bullets.empty()
        self.superbullets.empty()
        self.lazers.empty()
        self.explosions.empty()

        # Positioning the ship in center
        self._create_alien()
        self.ship.center_ship()

        # Restoring ship health
        self._renew_health_bar()

        # Hiding cursor
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Reaction to keydown"""

        if event.key == pygame.K_LSHIFT and not self.settings.sound_on:
            self.settings.play_sound_effect("press_button")

            # Changing image from sound on to mute
            # As the next click on this button is to mute
            mute_image = pygame.image.load("images/mute_button.png")
            self.sound_button.image.blit(mute_image, [0, 0])
            self.settings.sound_on = True
        elif event.key == pygame.K_LSHIFT and self.settings.sound_on:
            self.settings.play_sound_effect("press_button")

            # Changing image from mute to sound on
            # As the next click on this button is to turn the sound on
            sound_on_image = pygame.image.load("images/sound_on_button.png")
            self.sound_button.image.blit(sound_on_image, [0, 0])
            self.settings.sound_on = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_p:
            self._game_launch()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            with open("high_score.txt", "w") as file_object:
                file_object.write(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RSHIFT:
            self._fire_superbullet()

    def _check_keyup_events(self, event):
        """Reaction to keyup"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creating new bullet and adding it into bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if self.settings.sound_on:
                self.settings.play_sound_effect("shoot_bullet")

    def _fire_superbullet(self):
        """Creating new superbullet and adding it into superbullet group"""
        if len(self.superbullets) < self.settings.superbullets_allowed:
            new_superbullet = Superbullet(self)
            self.superbullets.add(new_superbullet)
            if self.settings.sound_on:
                self.settings.play_sound_effect("shoot_superbullet")

    def _update_bullets(self):
        """Renewing bullets position and removing old ones"""
        self.bullets.update()

        # Removing bullets outside the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            # Checking bullet-alien collision
            collisions = pygame.sprite.spritecollide(bullet, self.aliens, True)

            # Running explosion animation
            for collision in collisions:
                bullet.kill()
                explosion = Explosion(self, collision.rect.center, "small")
                self.explosions.add(explosion)
                self.stats.score += self.settings.alien_points_bullet
                self.scoreboard.prep_score()
                self.scoreboard.check_high_score()
                if self.settings.sound_on:
                    self.settings.play_sound_effect("small_explosion")

        if not self.aliens:
            self._start_new_level()

    def _update_superbullets(self):
        """Renewing superbullets position and removing old ones"""
        self.superbullets.update()

        # Removing superbullets outside the screen
        for superbullet in self.superbullets.copy():
            if superbullet.rect.bottom <= 0:
                self.superbullets.remove(superbullet)

            # Checking superbullet-alien collision
            collisions = pygame.sprite.spritecollide(superbullet, self.aliens, True)

            # Running explosion animation
            for collision in collisions:
                explosion = Explosion(self, collision.rect.center, "big")
                self.explosions.add(explosion)
                self.stats.score += self.settings.alien_points_superbullet
                self.scoreboard.prep_score()
                self.scoreboard.check_high_score()
                if self.settings.sound_on:
                    self.settings.play_sound_effect("big_explosion")

        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """Initializing new level settings"""
        self._create_alien()
        self.bullets.empty()
        self.settings.increase_speed()
        for alien in self.aliens.sprites():
            alien.increase_alien_speed()

        # Level increase
        self.stats.level += 1
        self.scoreboard.prep_level()

        if self.settings.sound_on:
            self.settings.play_sound_effect("new_level")

    def _update_explosions(self):
        self.explosions.update()

    def _create_alien(self):
        """Creating an alien"""
        for alien in range(9):
            alien = Alien(self)
            self.aliens.add(alien)

    def _update_aliens(self):
        """Updating alien position"""
        self.aliens.update()

        # Checking for collisions between spaceship and alien ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Checking for alien ship to get to the bottom of the screen
        self._check_aliens_bottom()

    def _shoot_lazers(self):
        """Creating new lazer and controlling time between lazer shoots"""
        # Recording current time
        time_now = pygame.time.get_ticks()
        last_lazer_shoot = self.settings.last_lazer_shoot
        cooldown = self.settings.lazer_cooldown
        lazers = len(self.lazers)
        aliens = len(self.aliens)

        # Shooting
        if time_now - last_lazer_shoot > cooldown and lazers < 5 and aliens > 0:
            attacking_alien = random.choice(self.aliens.sprites())
            lazer = Lazer(
                self, attacking_alien.rect.centerx, attacking_alien.rect.bottom
            )
            self.lazers.add(lazer)
            self.settings.last_lazer_shoot = time_now
            if self.settings.sound_on:
                self.settings.play_sound_effect("shoot_alien_lazer")

    def _check_lazer_position(self):
        """Renewing lazer position on the screen and checking for collisions with the ship"""  # noqa
        # Renewing lazers position and removing old ones
        self.lazers.update()

        # Removing lazers outside the screen
        for lazer in self.lazers.copy():
            if lazer.rect.top >= self.settings.screen_height:
                self.lazers.remove(lazer)

            # Checking lazer-ship collision and running explosion animation
            if pygame.sprite.spritecollideany(self.ship, self.lazers):
                lazer.kill()
                explosion = Explosion(self, self.ship.rect.center, "very_small")
                self.explosions.add(explosion)
                self.ship.health_remaining -= 1
                if self.settings.sound_on:
                    self.settings.play_sound_effect("ship_hit")

    def _draw_health_bar(self):
        """Drawing spaceship health bar"""
        bar_x = self.ship.rect.x
        bar_y = self.ship.rect.bottom + 10
        bar_width = self.ship.rect.width
        bar_height = 15
        pygame.draw.rect(
            self.screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height)
        )

    def _update_ship_health(self):
        """Updating health bar"""
        if self.ship.health_remaining > 0:
            bar_x = self.ship.rect.x
            bar_y = self.ship.rect.bottom + 10
            bar_height = 15
            bar_width = int(
                self.ship.rect.width
                * ((self.ship.health_remaining / self.ship.health_start))
            )
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                ((bar_x, bar_y, bar_width, bar_height)),  # noqa
            )
        elif self.ship.health_remaining <= 0:
            if self.stats.ships_left > 0:
                self.stats.ships_left -= 1
                self._renew_health_bar()
                self.scoreboard.prep_ships()
            else:
                self.aliens.empty()
                self.bullets.empty()
                self.superbullets.empty()

                self.ship.center_ship()
                self._renew_health_bar()

                self.stats.game_active = False
                pygame.mouse.set_visible(True)

    def _renew_health_bar(self):
        self.ship.health_remaining = 3

    def _ship_hit(self):
        """Processing alien-starship collision"""
        # Creating explosion
        ship_explosion = Explosion(self, self.ship.rect.center, "big")
        self.explosions.add(ship_explosion)

        if self.stats.ships_left > 0:
            # Decreasing number of ships left
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Clearing alien and (super)bullets groups
            self.aliens.empty()
            self.bullets.empty()
            self.superbullets.empty()

            # Positioning new ship in the center
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        if self.settings.sound_on:
            self.settings.play_sound_effect("big_explosion")

    def _check_aliens_bottom(self):
        """Checking for alien ship to get to the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()

    def _create_starry_sky(self):
        """Creating starry sky"""
        star = Star(self)
        star_width, star_height = star.rect.size

        available_space_x = self.settings.screen_width - star_width
        number_of_stars = available_space_x // star_width

        available_space_y = self.settings.screen_height - star_height
        number_of_rows = available_space_y // star_height

        for row_number in range(number_of_rows):
            for star_number in range(number_of_stars):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """Creating star and its placement"""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = random.randint(-50, 50) + 5 * star_width * star_number
        star.rect.x = star.x
        star.rect.y = (
            random.randint(-50, 50) + 5 * star.rect.height * row_number
        )  # noqa
        self.stars.add(star)

    def _update_screen(self):
        # Tracing screen for every cycle
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        self._draw_health_bar()
        self._update_ship_health()
        self.bullets.draw(self.screen)
        self.superbullets.draw(self.screen)
        self.explosions.draw(self.screen)
        self.aliens.draw(self.screen)
        self.lazers.draw(self.screen)
        self.scoreboard.show_score()
        self.sound_button.draw_button()

        # Displaying Play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Displaying of the last traced screen
        pygame.display.flip()
