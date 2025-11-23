class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        #从文件中拉取历史最高分
        try :
            with open("high_score.txt", "r") as f:
                self.high_score = int(f.read())
        except :
            self.high_score = 0
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_highscore(self):
        """保存最高分"""
        with open("high_score.txt","w") as h:
            h.write(str(self.high_score))