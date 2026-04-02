"""
Player model for Space Invaders.
This class represents the player ship and handles movement and shooting.
"""

from .constants import PLAYER_ICON
from .Bullet import Bullet


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = PLAYER_ICON

    def move(self, direction):
        """Move the player horizontally if the destination is inside bounds."""
        new_x = self.x + direction
        if 0 <= new_x < self.game.width:
            self.x = new_x

    def shoot(self):
        """Create a new player bullet and add it to the game state."""
        new_bullet = Bullet(self.game, self.x, self.y - 1)
        self.game.bullets.append(new_bullet)
