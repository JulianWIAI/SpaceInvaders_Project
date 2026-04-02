"""
Game model for Space Invaders.
This class manages game state, alien and bullet updates, collisions, and victory conditions.
"""

import random
from .Player import Player
from .Alien import Alien
from .AlienBullet import AlienBullet


class Game:
    def __init__(self, width, height, hit_sound, alien_shoot_sound):
        self.width = width
        self.height = height
        self.player = Player(self, width // 2, height - 2)
        self.bullets = []
        self.aliens = []
        self.alien_direction = 1
        self.game_over = False
        self.score = 0
        self.hit_sound = hit_sound
        self.alien_shoot_sound = alien_shoot_sound
        self.alien_bullets = []
        self.alien_shoot_timer = 0
        self.alien_shoot_interval = 60
        self.alien_move_timer = 0
        self.alien_move_interval = 20
        self.setup_aliens()

    def setup_aliens(self):
        """Initialize alien positions in a grid pattern."""
        for y in range(3):
            for x in range(1, self.width - 2, 2):
                self.aliens.append(Alien(self, x, y + 1))

    def update_game_state(self):
        """Update all active objects and evaluate win/loss conditions."""
        if self.game_over:
            return

        self._update_player_bullets()
        self._move_aliens()
        self._update_alien_bullets()
        self._check_player_collision()
        self._check_victory()

    def _update_player_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_out_of_bounds():
                self.bullets.remove(bullet)
            else:
                collided = False
                for alien in self.aliens[:]:
                    if bullet.x == alien.x and bullet.y == alien.y:
                        self.aliens.remove(alien)
                        self.score += 10
                        self.hit_sound.play()
                        collided = True
                        remaining_aliens = len(self.aliens)
                        if remaining_aliens < 5:
                            self.alien_move_interval = 5
                        elif remaining_aliens < 10:
                            self.alien_move_interval = 10
                        elif remaining_aliens < 18:
                            self.alien_move_interval = 15
                        break
                if collided:
                    self.bullets.remove(bullet)

    def _move_aliens(self):
        self.alien_move_timer += 1
        if self.alien_move_timer >= self.alien_move_interval:
            self.alien_move_timer = 0
            move_down = False
            for alien in self.aliens:
                if (self.alien_direction == 1 and alien.x >= self.width - 1) or \
                        (self.alien_direction == -1 and alien.x <= 0):
                    move_down = True
                    break
            if move_down:
                self.alien_direction *= -1
                for alien in self.aliens:
                    alien.move(0, 1)
                    if alien.y >= self.player.y:
                        self.game_over = True
            else:
                for alien in self.aliens:
                    alien.move(self.alien_direction, 0)

    def _update_alien_bullets(self):
        for bullet in self.alien_bullets[:]:
            bullet.move()
            if bullet.is_out_of_bounds():
                self.alien_bullets.remove(bullet)
        self.alien_shoot_timer += 1
        if self.alien_shoot_timer >= self.alien_shoot_interval and self.aliens:
            self.alien_shoot_timer = 0
            shooting_alien = random.choice(self.aliens)
            new_bullet = AlienBullet(self, shooting_alien.x, shooting_alien.y + 1)
            self.alien_bullets.append(new_bullet)
            self.alien_shoot_sound.play()

    def _check_player_collision(self):
        for bullet in self.alien_bullets[:]:
            if bullet.x == self.player.x and bullet.y == self.player.y:
                self.alien_bullets.remove(bullet)
                self.game_over = True
                break

    def _check_victory(self):
        if not self.aliens and not self.game_over:
            self.game_over = True
            print("!!! YOU WON !!!")
        if self.game_over:
            print("--- GAME OVER ---")
