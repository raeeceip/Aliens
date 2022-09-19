import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """Class to create an explosion"""

    def __init__(self, ai_game, center, size):
        super().__init__()

        # Creating a list to store explosion images to create animation
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"images/exp{num}.png")
            if size == "very_small":
                img = pygame.transform.scale(img, (60, 60))
            if size == "small":
                img = pygame.transform.scale(img, (80, 80))
            if size == "big":
                img = pygame.transform.scale(img, (120, 120))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # Assigning explosion position
        self.rect.center = center

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):

        now = pygame.time.get_ticks()

        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
