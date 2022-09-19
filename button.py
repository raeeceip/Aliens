import pygame


class Button:
    def __init__(self, ai_game, effect):
        """Initialising button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        if effect == "play":
            self.image = pygame.image.load("images/play_button.png")
        # Sound button - by default it is a mute button image
        # As the sound is on and mute button is for turning the sound off
        elif effect == "sound":
            self.image = pygame.image.load("images/mute_button.png")

        self.rect = self.image.get_rect()

        # Button placement
        if effect == "play":
            self.rect.center = self.screen_rect.center
        elif effect == "sound":
            self.rect = self.image.get_rect()
            self.rect.left = self.screen_rect.left + 10
            self.rect.top = 120

    def draw_button(self):
        """Drawing play button on the screen"""
        self.screen.blit(self.image, self.rect)
