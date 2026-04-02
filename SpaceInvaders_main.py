"""Main entry point for Space Invaders.
This module launches the game, manages screen states, and handles highscore persistence.
"""

import os
import pygame
import json

from SBS.constants import (
    BOARD_WIDTH,
    BOARD_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BLACK,
    WHITE,
    GREY,
    PLAYER_IMAGE_PATH,
    ALIEN_IMAGE_PATH,
    BULLET_IMAGE_PATH,
    GAME_OVER_IMAGE_PATH,
    WIN_IMAGE_PATH,
    ALIEN_BULLET_IMAGE_PATH,
    ICON_IMAGE_PATH,
    MUSIC_PATH,
    SHOOT_SOUND_PATH,
    HIT_SOUND_PATH,
    GAME_OVER_SOUND_PATH,
    ALIEN_SHOOT_SOUND_PATH,
    HIGHSCORE_FILE,
    MAX_HIGHSCORES,
    MAX_NAME_LENGTH,
)
from SBS.Game import Game
from SBS.PygameRenderer import PygameRenderer

# ==========================================
# --- HIGHSCORE FUNCTIONS ---
# ==========================================

def load_highscores(file):
    """Load the highscore list (now with names and scores)."""
    try:
        with open(file, 'r') as f:
            scores = json.load(f)

            # If the list is empty, return it
            if not scores:
                return []

            # CHECK: Is this the old structure (only numbers)?
            if not isinstance(scores[0], dict):
                print("Old highscore file format detected. Resetting.")
                return []

            # Wenn wir hier sind, ist die Struktur korrekt
            return scores

    except (FileNotFoundError, json.JSONDecodeError):
        # File not found or corrupted; start with an empty list
        return []


def save_highscores(file, scores_list, new_entry, max_scores):
    """Add a new entry, sort the highscores, trim the list, and save."""
    scores_list.append(new_entry)
    # Sort the list in descending order by score
    scores_list.sort(key=lambda item: item['score'], reverse=True)
    # Trim the list to the maximum size
    updated_scores = scores_list[:max_scores]

    with open(file, 'w') as f:
        json.dump(updated_scores, f, indent=4)

    return updated_scores


def reset_highscores(file):
    """Clear all highscores and save an empty list."""
    with open(file, 'w') as f:
        json.dump([], f)
    return []


# ==========================================
# --- 3. THE CONTROLLER (Game Loop) ---
# (Completely reorganized for clearer state management)
# ==========================================

def main_pygame():
    """Main function with state-machine management."""

    # --- Initialisierung ---
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    try:
        icon_surface = pygame.image.load(ICON_IMAGE_PATH).convert_alpha()
        pygame.display.set_icon(icon_surface)
    except pygame.error:
        pass

    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    # --- Sounds laden ---
    try:
        pygame.mixer.music.load(MUSIC_PATH)
        shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
        hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH)
        game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_PATH)
        alien_shoot_sound = pygame.mixer.Sound(ALIEN_SHOOT_SOUND_PATH)
    except pygame.error as e:
        print(f"!!! FEHLER BEIM LADEN EINES SOUNDS: {e}")

        class DummySound:
            def play(self): pass

        shoot_sound, hit_sound, game_over_sound, alien_shoot_sound = DummySound(), DummySound(), DummySound(), DummySound()

    # --- Game variables ---
    storage_dir = os.path.dirname(HIGHSCORE_FILE)
    if storage_dir:
        os.makedirs(storage_dir, exist_ok=True)
    highscores = load_highscores(HIGHSCORE_FILE)

    # Create the renderer once and keep the highscore list
    # The game object is assigned later
    renderer = PygameRenderer(None, screen, highscores)

    game = None  # The game object does not exist yet
    player_name = ""  # For player name input

    current_state = "START"  # Starting state
    running = True

    # --- MAIN GAME LOOP ---
    while running:

        # Poll all events (keyboard, mouse, etc.)
        events = pygame.event.get()

        # --- State management ---

        if current_state == "START":
            # --- Event handling for START ---
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter
                        if len(player_name) > 0:
                            # Start the game!
                            game = Game(BOARD_WIDTH, BOARD_HEIGHT, hit_sound, alien_shoot_sound)
                            renderer.game = game  # Assign the game object to the renderer
                            current_state = "PLAY"
                            pygame.mixer.music.play(-1)  # Start the background music
                    elif event.key == pygame.K_BACKSPACE:  # Backspace
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_x:  # Highscore reset
                        highscores = reset_highscores(HIGHSCORE_FILE)
                        renderer.highscores = highscores  # Update renderer highscore list
                    else:
                        # Regular character input
                        if len(player_name) < MAX_NAME_LENGTH:
                            player_name += event.unicode.upper()  # Append the uppercase character

            # --- Draw START screen ---
            renderer.draw_start_screen(player_name)


        elif current_state == "PLAY":
            # --- Event handling for PLAY ---
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        game.player.move(-1)
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        game.player.move(1)
                    elif event.key == pygame.K_s or event.key == pygame.K_SPACE:
                        game.player.shoot()
                        shoot_sound.play()
                    if event.key == pygame.K_q:
                        running = False

            # --- Logic update for PLAY ---
            game.update_game_state()

            # --- Draw for PLAY ---
            renderer.draw_game_screen()  # Uses the new rendering function

            # --- State transition check ---
            if game.game_over:
                pygame.mixer.music.stop()
                game_over_sound.play()
                # Save highscore
                new_entry = {"name": player_name, "score": game.score}
                highscores = save_highscores(HIGHSCORE_FILE, highscores, new_entry, MAX_HIGHSCORES)
                renderer.highscores = highscores  # Update renderer highscore list
                current_state = "GAME_OVER"


        elif current_state == "GAME_OVER":
            # --- Event handling for GAME_OVER ---
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_r:
                        # Return to the start screen
                        player_name = ""  # Reset the player name
                        current_state = "START"

            # --- Draw for GAME_OVER ---
            # Use the same draw function; it displays the game over overlay
            # automatically when game.game_over is True.
            renderer.draw_game_screen()

        # --- Allgemeines Update ---
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main_pygame()