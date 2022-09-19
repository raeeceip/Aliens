import pygame


class Settings:
    """Class to store all the game settings"""

    def __init__(self):
        """Initializing static game settings"""

        pygame.init()
        pygame.mixer.init()

        # Screen parameters
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (16, 16, 61)

        # Sound parameters
        self.sound_on = True

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullets_allowed = 5

        # Superbullet settings
        self.superbullets_allowed = 1

        # Lazer cooldown in milliseconds
        self.lazer_cooldown = 1000

        # Controlling time between lazer shoots
        self.last_lazer_shoot = pygame.time.get_ticks()

        # Game speed acceleration
        self.speedup_scale = 1.1

        # Amount of points is increasing depending on speed acceleration
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializing settings, that change during the game"""
        self.ship_speed_factor = 9.0
        self.bullet_speed_factor = 10.0
        self.superbullet_speed_factor = 12.0
        self.lazer_speed_factor = 10.0

        # Score count
        self.alien_points_bullet = 50
        self.alien_points_superbullet = 25

    def increase_speed(self):
        """Increasing speed settings and amount of points"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.superbullet_speed_factor *= self.speedup_scale
        self.lazer_speed_factor *= self.speedup_scale
        self.alien_points_bullet = int(
            self.alien_points_bullet * self.score_scale
        )  # noqa
        self.alien_points_superbullet = int(
            self.alien_points_superbullet * self.score_scale
        )

    def play_sound_effect(self, effect):
        """Initializing sound effects"""
        if effect == "shoot_bullet":
            self.bullet_sound = pygame.mixer.Sound("sounds/bullet_sound")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
        elif effect == "shoot_superbullet":
            self.bullet_sound = pygame.mixer.Sound("sounds/superbullet_sound")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
        elif effect == "shoot_alien_lazer":
            self.bullet_sound = pygame.mixer.Sound("sounds/alien_lazer")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
        elif effect == "small_explosion":
            self.bullet_sound = pygame.mixer.Sound("sounds/small_explosion")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
        elif effect == "big_explosion":
            self.bullet_sound = pygame.mixer.Sound("sounds/big_explosion")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
        elif effect == "press_button":
            self.bullet_sound = pygame.mixer.Sound("sounds/button_pressed")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
        elif effect == "new_level":
            self.bullet_sound = pygame.mixer.Sound("sounds/new_level")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
        elif effect == "ship_hit":
            self.bullet_sound = pygame.mixer.Sound("sounds/ship_hit")
            self.bullet_sound.set_volume(0.15)
            self.bullet_sound.play()
