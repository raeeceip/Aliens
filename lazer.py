import pygame
from pygame.sprite import Sprite


class Lazer(Sprite):
    """Class for controlling alien lazers"""

    def __init__(self, ai_game, x, y):
        """Creating lazer  at an alien ship current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Creating lazer
        self.image = pygame.image.load("images/lazer.png")
        self.rect = self.image.get_rect()

        self.rect.center = [x, y]

    def update(self):
        """Moving lazer downwards"""
        self.rect.y += self.settings.lazer_speed_factor
