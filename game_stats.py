class GameStats:
    """Collecting statistics for the game"""

    def __init__(self, ai_game):
        """Initialising statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Game starts in non-active state
        self.game_active = False

        with open("high_score.txt", "w+") as file_object:
            high_score = file_object.read()
            if high_score == "":
                high_score = 0

        self.high_score = int(high_score)

    def reset_stats(self):
        """Initialising statistics, changing in game process"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
