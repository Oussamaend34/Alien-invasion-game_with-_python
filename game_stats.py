class GameStats():
    """Track statistics for alien invasion."""
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_stats = False

    def reset_stats(self):
        """Initialize statistics that can change during game."""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
