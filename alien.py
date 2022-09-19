import pygame
from pygame.sprite import Sprite

from random import randrange


class Alien(Sprite):
    """Class to create one alien"""

    def __init__(self, ai_game):
        """Initializing alien and its starting point"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Loading alien image and assigning rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Assigning starting position
        self.rect.x = randrange(self.settings.screen_width - self.rect.width)
        self.rect.bottom = randrange(-80, -20)

        # Speed settings
        self.alien_speed_factor_x = 1.0
        self.alien_speed_factor_y = randrange(-8, -6)
        self.alien_drop_speed = 10
        self.alien_speed_up_scale = 0.9

        # Alien_direction: 1 - to the right, -1 - to the left
        self.alien_direction = 1

    def check_edges(self):
        """Returns True if alien if at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Moving alien randomly on the screen"""
        self.rect.x += self.alien_speed_factor_x * self.alien_direction
        self.rect.y += self.alien_speed_factor_y
        if self.check_edges:
            self.rect.y += self.alien_drop_speed
            self.alien_direction *= -1

    def increase_alien_speed(self):
        self.alien_speed_factor_y *= self.alien_speed_up_scale
