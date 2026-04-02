"""
Renderer module for Space Invaders.
This class handles all drawing operations for the start screen, game board, and end screen.
"""

import pygame
from .constants import (
    SCALE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BLACK,
    WHITE,
    GREY,
    PLAYER_IMAGE_PATH,
    ALIEN_IMAGE_PATH,
    BULLET_IMAGE_PATH,
    ALIEN_BULLET_IMAGE_PATH,
    GAME_OVER_IMAGE_PATH,
    WIN_IMAGE_PATH,
)


class PygameRenderer:
    def __init__(self, game_object, screen, highscores_list):
        self.game = game_object
        self.screen = screen
        self.highscores = highscores_list

        self.font_title = pygame.font.Font(None, 60)
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)

        try:
            player_img_original = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
            self.player_image = pygame.transform.scale(player_img_original, (SCALE, SCALE))

            alien_img_original = pygame.image.load(ALIEN_IMAGE_PATH).convert_alpha()
            self.alien_image = pygame.transform.scale(alien_img_original, (SCALE, SCALE))

            bullet_img_original = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
            self.bullet_image = pygame.transform.scale(bullet_img_original, (SCALE // 4, SCALE // 2))

            alien_bullet_img_original = pygame.image.load(ALIEN_BULLET_IMAGE_PATH).convert_alpha()
            self.alien_bullet_image = pygame.transform.scale(alien_bullet_img_original, (SCALE // 4, SCALE // 2))

            game_over_img_original = pygame.image.load(GAME_OVER_IMAGE_PATH).convert_alpha()
            self.game_over_image = pygame.transform.scale(
                game_over_img_original,
                (int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.2)),
            )

            win_img_original = pygame.image.load(WIN_IMAGE_PATH).convert_alpha()
            self.win_image = pygame.transform.scale(
                win_img_original,
                (int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.2)),
            )
        except pygame.error as e:
            print(f"!!! ERROR LOADING IMAGE: {e}")
            pygame.quit()
            exit()

    def draw_highscores(self, x_pos, y_pos):
        """Render the highscore list on the screen."""
        hs_title_text = self.font.render("HIGHSCORES", True, BLACK)
        hs_title_rect = hs_title_text.get_rect(topright=(x_pos, y_pos))
        self.screen.blit(hs_title_text, hs_title_rect)

        for i, entry in enumerate(self.highscores):
            hs_text = self.font_small.render(f"{i + 1}. {entry['name']} {entry['score']}", True, BLACK)
            hs_rect = hs_text.get_rect(topright=(x_pos, y_pos + 30 + i * 20))
            self.screen.blit(hs_text, hs_rect)

    def draw_start_screen(self, player_name):
        """Draw the welcome screen and name input prompt."""
        self.screen.fill(WHITE)

        title_text = self.font_title.render("SPACE INVADERS", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)

        prompt_text = self.font.render("ENTER NAME:", True, BLACK)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(prompt_text, prompt_rect)

        name_box_width = 100
        name_box_rect = pygame.Rect(
            (SCREEN_WIDTH - name_box_width) // 2,
            SCREEN_HEIGHT // 2,
            name_box_width,
            30,
        )
        pygame.draw.rect(self.screen, GREY, name_box_rect, 2)

        cursor_visible = pygame.time.get_ticks() // 500 % 2 == 0
        name_to_show = player_name
        if cursor_visible:
            name_to_show += "_"

        name_text = self.font.render(name_to_show, True, BLACK)
        name_rect = name_text.get_rect(center=name_box_rect.center)
        self.screen.blit(name_text, name_rect)

        instructions_text = self.font_small.render("Press Enter to start | X to reset highscores", True, GREY)
        instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions_text, instructions_rect)

        self.draw_highscores(SCREEN_WIDTH - 10, 10)

    def draw_game_screen(self):
        """Render the main gameplay screen and game over overlays."""
        self.screen.fill(WHITE)

        player_rect = pygame.Rect(self.game.player.x * SCALE, self.game.player.y * SCALE, SCALE, SCALE)
        self.screen.blit(self.player_image, player_rect)

        for alien in self.game.aliens:
            alien_rect = pygame.Rect(alien.x * SCALE, alien.y * SCALE, SCALE, SCALE)
            self.screen.blit(self.alien_image, alien_rect)

        for bullet in self.game.bullets:
            bullet_width, bullet_height = self.bullet_image.get_size()
            bullet_x = bullet.x * SCALE + (SCALE - bullet_width) // 2
            bullet_y = bullet.y * SCALE
            self.screen.blit(self.bullet_image, (bullet_x, bullet_y))

        for bullet in self.game.alien_bullets:
            bullet_width, bullet_height = self.alien_bullet_image.get_size()
            bullet_x = bullet.x * SCALE + (SCALE - bullet_width) // 2
            bullet_y = bullet.y * SCALE
            self.screen.blit(self.alien_bullet_image, (bullet_x, bullet_y))

        score_text = self.font.render(f"SCORE: {self.game.score}", True, BLACK)
        self.screen.blit(score_text, (5, 5))

        self.draw_highscores(SCREEN_WIDTH - 10, 10)

        if self.game.game_over:
            if not self.game.aliens:
                image_to_draw = self.win_image
            else:
                image_to_draw = self.game_over_image
            image_rect = image_to_draw.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(image_to_draw, image_rect)

            replay_text = self.font_small.render("Press R to return to menu or Q to quit", True, BLACK)
            text_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, image_rect.bottom + 30))
            self.screen.blit(replay_text, text_rect)
