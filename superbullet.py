import pygame
from pygame.sprite import Sprite


class Superbullet(Sprite):
    """Class to control ship bullets"""

    def __init__(self, ai_game):
        """Creating superbullet object at the ship current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Creating superbullet
        self.image = pygame.image.load("images/superbullet.png")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height

        # Make superbullet fire from the top of the spaceship
        self.rect.midbottom = ai_game.ship.rect.midtop

        # Storing superbullet position in float
        self.y = float(self.rect.y)

    def update(self):
        """Moving superbullet upwards"""

        # Renewing superbullet position in float format
        self.y -= self.settings.superbullet_speed_factor

        # Renewing rect position
        self.rect.y = self.y
