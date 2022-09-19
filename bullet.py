import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class for controlling ship bullets"""

    def __init__(self, ai_game):
        """Creating bullet object at the ship current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Creating bullet
        self.image = pygame.image.load("images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height

        # Making bullet fire from the top of the spaceship
        self.rect.midbottom = ai_game.ship.rect.midtop

        # Storing bullet position in float
        self.y = float(self.rect.y)

    def update(self):
        """Moving bullet upwards"""

        # Renewing bullet position in float format
        self.y -= self.settings.bullet_speed_factor

        # Renewing rect position
        self.rect.y = self.y
