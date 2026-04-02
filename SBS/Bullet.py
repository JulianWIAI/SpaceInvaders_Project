"""
Bullet model for Space Invaders.
This class represents a shot fired by the player ship.
"""

from .constants import BULLET_ICON


class Bullet:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = BULLET_ICON

    def move(self):
        """Advance the bullet upward by one unit."""
        self.y -= 1

    def is_out_of_bounds(self):
        """Return True when the bullet leaves the top of the screen."""
        return self.y < 0
