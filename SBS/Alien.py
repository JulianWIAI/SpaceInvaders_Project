"""
Alien model for Space Invaders.
This class represents an enemy unit and supports movement along the board.
"""

from .constants import ALIEN_ICON


class Alien:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = ALIEN_ICON

    def move(self, dx, dy):
        """Move the alien by the given delta values."""
        self.x += dx
        self.y += dy
