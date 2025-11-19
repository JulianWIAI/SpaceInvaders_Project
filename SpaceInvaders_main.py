import os
import time
import pygame
import json
import random

# --- KONSTANTEN ---
BOARD_WIDTH = 20
BOARD_HEIGHT = 15

SCALE = 30
SCREEN_WIDTH = BOARD_WIDTH * SCALE
SCREEN_HEIGHT = BOARD_HEIGHT * SCALE
FPS = 30

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)  # Neu für den Startbildschirm

# === BILDER-KONSTANTEN ===
ASSETS_FOLDER = "assets"
# ... (alle deine Bild-Konstanten bleiben gleich) ...
PLAYER_IMAGE_NAME = "player_spaceship.png"
ALIEN_IMAGE_NAME = "alien_spaceship.png"
BULLET_IMAGE_NAME = "bullet_laser.png"
GAME_OVER_IMAGE_NAME = "game_over.png"
WIN_IMAGE_NAME = "win.png"
ALIEN_BULLET_IMAGE_NAME = "alien_bullet.png"

PLAYER_IMAGE_PATH = os.path.join(ASSETS_FOLDER, PLAYER_IMAGE_NAME)
ALIEN_IMAGE_PATH = os.path.join(ASSETS_FOLDER, ALIEN_IMAGE_NAME)
BULLET_IMAGE_PATH = os.path.join(ASSETS_FOLDER, BULLET_IMAGE_NAME)
GAME_OVER_IMAGE_PATH = os.path.join(ASSETS_FOLDER, GAME_OVER_IMAGE_NAME)
WIN_IMAGE_PATH = os.path.join(ASSETS_FOLDER, WIN_IMAGE_NAME)
ALIEN_BULLET_IMAGE_PATH = os.path.join(ASSETS_FOLDER, ALIEN_BULLET_IMAGE_NAME)

# --- SOUND-KONSTANTEN ---
# ... (alle deine Sound-Konstanten bleiben gleich) ...
MUSIC_PATH = os.path.join(ASSETS_FOLDER, "background_music.wav")
SHOOT_SOUND_PATH = os.path.join(ASSETS_FOLDER, "shoot.wav")
HIT_SOUND_PATH = os.path.join(ASSETS_FOLDER, "hit.wav")
GAME_OVER_SOUND_PATH = os.path.join(ASSETS_FOLDER, "game_over.wav")
ALIEN_SHOOT_SOUND_PATH = os.path.join(ASSETS_FOLDER, "alien_shoot.wav")

# --- HIGHSCORE-KONSTANTEN ---
HIGHSCORE_FILE = "highscore.json"
MAX_HIGHSCORES = 5
MAX_NAME_LENGTH = 3  # Beschränken wir den Namen auf 3 Buchstaben (klassisch)

# --- NEU: WIEDER HINZUGEFÜGTE PLATZHALTER ---
# (Diese wurden versehentlich gelöscht, werden aber intern von den Klassen noch gebraucht)
PLAYER_ICON = 'A'
ALIEN_ICON = 'M'
BULLET_ICON = '|'
EMPTY_SPACE = ' '
# --- ENDE ---

# ... (Alle deine Spiel-Klassen: Game, Player, Alien, Bullet, AlienBullet bleiben EXAKT GLEICH) ...
# ... (Ich füge sie hier ein, damit der Code wirklich komplett ist) ...

# ==========================================
# --- HIGHSCORE-FUNKTIONEN (STARK GEÄNDERT) ---
# ==========================================

def load_highscores(file):
    """Lädt die Highscore-Liste (jetzt mit Namen und Scores)."""
    try:
        with open(file, 'r') as f:
            scores = json.load(f)

            # Wenn die Liste leer ist, gib sie zurück
            if not scores:
                return []

            # PRÜFUNG: Ist es die alte Struktur (nur Zahlen)?
            if not isinstance(scores[0], dict):
                print("Alte Highscore-Datei erkannt. Wird zurückgesetzt.")
                return []  # KORREKTUR: Einfach leere Liste zurückgeben

            # Wenn wir hier sind, ist die Struktur korrekt
            return scores

    except (FileNotFoundError, json.JSONDecodeError):
        # Datei nicht gefunden oder komplett kaputt, starte mit leerer Liste
        return []


def save_highscores(file, scores_list, new_entry, max_scores):
    """Fügt einen neuen Eintrag (dict) hinzu, sortiert, kürzt und speichert."""
    scores_list.append(new_entry)
    # Sortiere die Liste absteigend nach dem 'score'-Wert
    scores_list.sort(key=lambda item: item['score'], reverse=True)
    # Kürze die Liste auf die maximale Anzahl
    updated_scores = scores_list[:max_scores]

    with open(file, 'w') as f:
        json.dump(updated_scores, f, indent=4)

    return updated_scores


# NEUE Funktion
def reset_highscores(file):
    """Löscht alle Highscores und speichert eine leere Liste."""
    with open(file, 'w') as f:
        json.dump([], f)
    return []


# ==========================================
# --- 1. DAS MODELL (Die Spiellogik) ---
# (Diese Klassen sind UNVERÄNDERT)
# ==========================================

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
        for y in range(3):
            for x in range(1, self.width - 2, 2):
                self.aliens.append(Alien(self, x, y + 1))

    def update_game_state(self):
        if self.game_over:
            return
        # 1. Spieler-Kugeln
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
        # 2. Aliens bewegen
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
        # 3. Alien-Kugeln
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
        # 4. Kollision Spieler
        for bullet in self.alien_bullets[:]:
            if bullet.x == self.player.x and bullet.y == self.player.y:
                self.alien_bullets.remove(bullet)
                self.game_over = True
                break
        # 5. Siegbedingung
        if not self.aliens and not self.game_over:
            self.game_over = True
            print("!!! DU HAST GEWONNEN !!!")
        if self.game_over:
            print("--- GAME OVER ---")


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = PLAYER_ICON

    def move(self, direction):
        new_x = self.x + direction
        if 0 <= new_x < self.game.width:
            self.x = new_x

    def shoot(self):
        new_bullet = Bullet(self, self.x, self.y - 1)
        self.game.bullets.append(new_bullet)


class Alien:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = ALIEN_ICON

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Bullet:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = BULLET_ICON

    def move(self):
        self.y -= 1

    def is_out_of_bounds(self):
        return self.y < 0


class AlienBullet:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.icon = 'v'

    def move(self):
        self.y += 1

    def is_out_of_bounds(self):
        return self.y >= self.game.height


# ==========================================
# --- 2. DIE VIEW (Die Darstellung) ---
# (STARK GEÄNDERT)
# ==========================================

class PygameRenderer:
    """
    Diese Klasse "malt" ALLES auf das Fenster.
    Sie hat jetzt zwei Zeichen-Modi: Startbildschirm und Spiel.
    """

    # GEÄNDERT: game_object startet als 'None'
    def __init__(self, game_object, screen, highscores_list):
        self.game = game_object
        self.screen = screen
        self.highscores = highscores_list

        # Schriften initialisieren
        self.font_title = pygame.font.Font(None, 60)  # Für Spieltitel
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)

        # === BILDER LADEN ===
        try:
            # (Der Code zum Laden aller 6 Bilder ist unverändert)
            player_img_original = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
            self.player_image = pygame.transform.scale(player_img_original, (SCALE, SCALE))
            alien_img_original = pygame.image.load(ALIEN_IMAGE_PATH).convert_alpha()
            self.alien_image = pygame.transform.scale(alien_img_original, (SCALE, SCALE))
            bullet_img_original = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
            self.bullet_image = pygame.transform.scale(bullet_img_original, (SCALE // 4, SCALE // 2))
            alien_bullet_img_original = pygame.image.load(ALIEN_BULLET_IMAGE_PATH).convert_alpha()
            self.alien_bullet_image = pygame.transform.scale(alien_bullet_img_original, (SCALE // 4, SCALE // 2))
            game_over_img_original = pygame.image.load(GAME_OVER_IMAGE_PATH).convert_alpha()
            self.game_over_image = pygame.transform.scale(game_over_img_original,
                                                          (int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.2)))
            win_img_original = pygame.image.load(WIN_IMAGE_PATH).convert_alpha()
            self.win_image = pygame.transform.scale(win_img_original,
                                                    (int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.2)))
        except pygame.error as e:
            print(f"!!! FEHLER BEIM LADEN EINES BILDES: {e}")
            pygame.quit()
            exit()
        # === ENDE BILDER LADEN ===

    def draw_highscores(self, x_pos, y_pos):
        """Hilfsfunktion, um Highscores zu zeichnen (wird 2x gebraucht)."""
        hs_title_text = self.font.render("HIGHSCORES", True, BLACK)
        hs_title_rect = hs_title_text.get_rect(topright=(x_pos, y_pos))
        self.screen.blit(hs_title_text, hs_title_rect)

        for i, entry in enumerate(self.highscores):
            # Zeige Name und Score
            hs_text = self.font_small.render(f"{i + 1}. {entry['name']} {entry['score']}", True, BLACK)
            hs_rect = hs_text.get_rect(topright=(x_pos, y_pos + 30 + i * 20))
            self.screen.blit(hs_text, hs_rect)

    # NEUE FUNKTION
    def draw_start_screen(self, player_name):
        """Zeichnet den Startbildschirm mit Namenseingabe."""
        self.screen.fill(WHITE)

        # Titel
        title_text = self.font_title.render("SPACE INVADERS", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)

        # Namenseingabe
        prompt_text = self.font.render("NAMEN EINGEBEN:", True, BLACK)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(prompt_text, prompt_rect)

        # Der Name selbst
        name_box_width = 100
        name_box_rect = pygame.Rect(
            (SCREEN_WIDTH - name_box_width) // 2,
            SCREEN_HEIGHT // 2,
            name_box_width, 30)
        pygame.draw.rect(self.screen, GREY, name_box_rect, 2)  # Box-Rand

        # Füge einen blinkenden Cursor hinzu (blinkt alle 0.5 Sek)
        cursor_visible = pygame.time.get_ticks() // 500 % 2 == 0
        name_to_show = player_name
        if cursor_visible:
            name_to_show += "_"

        name_text = self.font.render(name_to_show, True, BLACK)
        name_rect = name_text.get_rect(center=name_box_rect.center)
        self.screen.blit(name_text, name_rect)

        # Anweisungen
        instructions_text = self.font_small.render("Enter zum Starten | 'X' zum Highscore-Reset", True, GREY)
        instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions_text, instructions_rect)

        # Highscores auf dem Startbildschirm anzeigen
        self.draw_highscores(SCREEN_WIDTH - 10, 10)

    # STARK GEÄNDERT: Heißt jetzt 'draw_game_screen'
    def draw_game_screen(self):
        """Zeichnet den Haupt-Spielbildschirm (Spiel läuft oder Game Over)."""
        self.screen.fill(WHITE)

        # 1. Spieler
        player_rect = pygame.Rect(self.game.player.x * SCALE, self.game.player.y * SCALE, SCALE, SCALE)
        self.screen.blit(self.player_image, player_rect)
        # 2. Aliens
        for alien in self.game.aliens:
            alien_rect = pygame.Rect(alien.x * SCALE, alien.y * SCALE, SCALE, SCALE)
            self.screen.blit(self.alien_image, alien_rect)
        # 3. Kugeln (Spieler)
        for bullet in self.game.bullets:
            bullet_width, bullet_height = self.bullet_image.get_size()
            bullet_x = bullet.x * SCALE + (SCALE - bullet_width) // 2
            bullet_y = bullet.y * SCALE
            self.screen.blit(self.bullet_image, (bullet_x, bullet_y))
        # 3b. Kugeln (Alien)
        for bullet in self.game.alien_bullets:
            bullet_width, bullet_height = self.alien_bullet_image.get_size()
            bullet_x = bullet.x * SCALE + (SCALE - bullet_width) // 2
            bullet_y = bullet.y * SCALE
            self.screen.blit(self.alien_bullet_image, (bullet_x, bullet_y))

        # 4. Punktestand
        score_text = self.font.render(f"PUNKTE: {self.game.score}", True, BLACK)
        self.screen.blit(score_text, (5, 5))

        # 5. Highscores (mit neuer Struktur)
        self.draw_highscores(SCREEN_WIDTH - 10, 10)

        # 6. Game Over / Sieg Nachricht
        if self.game.game_over:
            if not self.game.aliens:
                image_to_draw = self.win_image
            else:
                image_to_draw = self.game_over_image
            image_rect = image_to_draw.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(image_to_draw, image_rect)

            replay_text = self.font_small.render("Drücke 'R' zum Menü oder 'Q' zum Beenden", True, BLACK)
            text_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, image_rect.bottom + 30))
            self.screen.blit(replay_text, text_rect)


# ==========================================
# --- 3. DER CONTROLLER (Die Spiel-Schleife) ---
# (KOMPLETT NEU STRUKTURIERT)
# ==========================================

def main_pygame():
    """Hauptfunktion mit Zustands-Management (State Machine)."""

    # --- Initialisierung ---
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    # --- Spiel-Variablen ---
    highscores = load_highscores(HIGHSCORE_FILE)

    # Renderer wird EINMAL erstellt und hält die Highscore-Liste
    # Das 'game'-Objekt wird ihm später zugewiesen
    renderer = PygameRenderer(None, screen, highscores)

    game = None  # Das Spiel-Objekt existiert noch nicht
    player_name = ""  # Für die Namenseingabe

    current_state = "START"  # Start-Zustand
    running = True

    # --- HAUPT-SPIEL-SCHLEIFE ---
    while running:

        # Hole alle Events (Tastatur, Maus, etc.)
        events = pygame.event.get()

        # --- Zustands-Verwaltung ---

        if current_state == "START":
            # --- Event-Handling für START ---
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter
                        if len(player_name) > 0:
                            # Spiel starten!
                            game = Game(BOARD_WIDTH, BOARD_HEIGHT, hit_sound, alien_shoot_sound)
                            renderer.game = game  # Renderer das Spiel-Objekt geben
                            current_state = "PLAY"
                            pygame.mixer.music.play(-1)  # Musik starten
                    elif event.key == pygame.K_BACKSPACE:  # Löschen
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_x:  # Highscore-Reset
                        highscores = reset_highscores(HIGHSCORE_FILE)
                        renderer.highscores = highscores  # Renderer-Liste aktualisieren
                    else:
                        # Normaler Buchstabe
                        if len(player_name) < MAX_NAME_LENGTH:
                            player_name += event.unicode.upper()  # Füge den Buchstaben hinzu (Groß)

            # --- Zeichnen für START ---
            renderer.draw_start_screen(player_name)


        elif current_state == "PLAY":
            # --- Event-Handling für PLAY ---
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

            # --- Logik-Update für PLAY ---
            game.update_game_state()

            # --- Zeichnen für PLAY ---
            renderer.draw_game_screen()  # Nutzt jetzt die neue Funktion

            # --- Zustands-Wechsel-Prüfung ---
            if game.game_over:
                pygame.mixer.music.stop()
                game_over_sound.play()
                # Highscore speichern
                new_entry = {"name": player_name, "score": game.score}
                highscores = save_highscores(HIGHSCORE_FILE, highscores, new_entry, MAX_HIGHSCORES)
                renderer.highscores = highscores  # Renderer-Liste aktualisieren
                current_state = "GAME_OVER"


        elif current_state == "GAME_OVER":
            # --- Event-Handling für GAME_OVER ---
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_r:
                        # Zurück zum Startbildschirm
                        player_name = ""  # Namen zurücksetzen
                        current_state = "START"

            # --- Zeichnen für GAME_OVER ---
            # Wir rufen dieselbe Funktion auf; sie zeigt dank game.game_over
            # automatisch den "Game Over"-Teil an.
            renderer.draw_game_screen()

        # --- Allgemeines Update ---
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main_pygame()