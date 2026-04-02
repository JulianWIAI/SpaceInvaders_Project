"""
Shared application constants used by the Space Invaders game.
This module centralizes display sizes, colors, asset paths, and gameplay limits.
"""

import os

BOARD_WIDTH = 20
BOARD_HEIGHT = 15
SCALE = 30
SCREEN_WIDTH = BOARD_WIDTH * SCALE
SCREEN_HEIGHT = BOARD_HEIGHT * SCALE
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

ASSETS_FOLDER = "assets"
PLAYER_IMAGE_NAME = "player_spaceship.png"
ALIEN_IMAGE_NAME = "alien_spaceship.png"
BULLET_IMAGE_NAME = "bullet_laser.png"
GAME_OVER_IMAGE_NAME = "game_over.png"
WIN_IMAGE_NAME = "win.png"
ALIEN_BULLET_IMAGE_NAME = "alien_bullet.png"
ICON_IMAGE_NAME = "icon.png"

PLAYER_IMAGE_PATH = os.path.join(ASSETS_FOLDER, PLAYER_IMAGE_NAME)
ALIEN_IMAGE_PATH = os.path.join(ASSETS_FOLDER, ALIEN_IMAGE_NAME)
BULLET_IMAGE_PATH = os.path.join(ASSETS_FOLDER, BULLET_IMAGE_NAME)
GAME_OVER_IMAGE_PATH = os.path.join(ASSETS_FOLDER, GAME_OVER_IMAGE_NAME)
WIN_IMAGE_PATH = os.path.join(ASSETS_FOLDER, WIN_IMAGE_NAME)
ALIEN_BULLET_IMAGE_PATH = os.path.join(ASSETS_FOLDER, ALIEN_BULLET_IMAGE_NAME)
ICON_IMAGE_PATH = os.path.join(ASSETS_FOLDER, ICON_IMAGE_NAME)

MUSIC_PATH = os.path.join(ASSETS_FOLDER, "background_music.wav")
SHOOT_SOUND_PATH = os.path.join(ASSETS_FOLDER, "shoot.ogg")
HIT_SOUND_PATH = os.path.join(ASSETS_FOLDER, "hit.ogg")
GAME_OVER_SOUND_PATH = os.path.join(ASSETS_FOLDER, "game_over.ogg")
ALIEN_SHOOT_SOUND_PATH = os.path.join(ASSETS_FOLDER, "alien_shoot.ogg")

HIGHSCORE_FILE = os.path.join("storage", "highscore.json")
MAX_HIGHSCORES = 5
MAX_NAME_LENGTH = 3

PLAYER_ICON = 'A'
ALIEN_ICON = 'M'
BULLET_ICON = '|'
EMPTY_SPACE = ' '
