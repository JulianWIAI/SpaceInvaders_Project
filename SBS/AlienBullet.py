"""
AlienBullet model for Space Invaders.
This class represents a shot fired by an enemy alien.
"""


class AlienBullet:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = 'v'

    def move(self):
        """Advance the alien bullet downward by one unit."""
        self.y += 1

    def is_out_of_bounds(self):
        """Return True when the alien bullet leaves the bottom of the screen."""
        return self.y >= self.game.height
