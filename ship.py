import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Class to control the ship"""

    def __init__(self, ai_game, health):
        """Initializing the ship and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height

        # Loading ship image
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Each new ship appears at the bottom of the screen above the health bar
        self.rect.midbottom = (
            int(self.screen_width / 2),
            self.screen_height - 100,
        )  # noqa

        # Save floating coordinates of the center of the ship
        self.x = float(self.rect.x)

        # Flag for moving
        self.moving_right = False
        self.moving_left = False

        # Health settings
        self.health_start = health
        self.health_remaining = health

    def update(self):
        """Updating ship position"""
        # Renewing x attribute, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor

        # Renew rect attribute based on self.x
        self.rect.x = self.x

    def blitme(self):
        """Draws the ship at the current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Position ship in the midbottom of the screen"""
        self.rect.midbottom = (
            int(self.screen_width / 2),
            self.screen_height - 100,
        )  # noqa
        self.x = float(self.rect.x)
