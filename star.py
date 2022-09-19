import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Class to create a star"""

    def __init__(self, ai_game):
        """Initializing star and its starting point"""
        super().__init__()
        self.screen = ai_game.screen

        self.image = pygame.image.load("images/star.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
