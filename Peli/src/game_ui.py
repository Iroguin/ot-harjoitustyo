"""UI for game."""
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

FONT_SMALL = None
FONT_MEDIUM = None
FONT_LARGE = None

STATE_MAIN_MENU = 0
STATE_GAME = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
STATE_LEADERBOARD = 4


class Button:
    """A clickable button for the UI."""

    def __init__(self, x, y, width, height, text, color=LIGHT_GRAY, hover_color=WHITE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        text_surface = FONT_MEDIUM.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


class ProgressBar:
    """A bar ui element for displaying health for example"""

    def __init__(self, x, y, width, height, value=100, max_value=100, color=GREEN, background=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.max_value = max_value
        self.color = color
        self.background = background

    def update(self, value):
        self.value = max(0, min(value, self.max_value))

    def draw(self, screen):
        pygame.draw.rect(screen, self.background, self.rect, border_radius=3)

        if self.value > 0:
            fill_width = int(self.rect.width * (self.value / self.max_value))
            fill_rect = pygame.Rect(
                self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, self.color, fill_rect, border_radius=3)

        pygame.draw.rect(screen, BLACK, self.rect, 1, border_radius=3)


class GameUI:
    """class for managing UI."""

    def __init__(self, screen_width, screen_height):
        global FONT_SMALL, FONT_MEDIUM, FONT_LARGE

        self.width = screen_width
        self.height = screen_height
        self.state = STATE_MAIN_MENU
        self.score = 0
        self.high_score = 0
        self.player_health = 100

        pygame.font.init()
        FONT_SMALL = pygame.font.SysFont("Arial", 16)
        FONT_MEDIUM = pygame.font.SysFont("Arial", 24)
        FONT_LARGE = pygame.font.SysFont("Arial", 48)

        self._create_main_menu()
        self._create_pause_menu()
        self._create_game_over_menu()
        self._create_leaderboard_menu()
        self._create_hud()

    def _create_main_menu(self):
        center_x = self.width // 2
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.height // 2 - button_height - button_spacing

        self.main_menu_buttons = [
            Button(center_x - button_width // 2, start_y,
                   button_width, button_height, "Start Game", BLUE, LIGHT_GRAY),
            Button(center_x - button_width // 2, start_y + button_height + button_spacing,
                   button_width, button_height, "Leaderboard", BLUE, LIGHT_GRAY),
            Button(center_x - button_width // 2, start_y + 2 * (button_height + button_spacing),
                   button_width, button_height, "Quit", RED, LIGHT_GRAY)
        ]

    def _create_pause_menu(self):
        center_x = self.width // 2
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.height // 2 - button_height - button_spacing

        self.pause_menu_buttons = [
            Button(center_x - button_width // 2, start_y,
                   button_width, button_height, "Resume", GREEN, LIGHT_GRAY),
            Button(center_x - button_width // 2, start_y + button_height + button_spacing,
                   button_width, button_height, "Main Menu", BLUE, LIGHT_GRAY),
            Button(center_x - button_width // 2, start_y + 2 * (button_height + button_spacing),
                   button_width, button_height, "Quit", RED, LIGHT_GRAY)
        ]

    def _create_game_over_menu(self):
        center_x = self.width // 2
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.height // 2 + 50

        self.game_over_buttons = [
            Button(center_x - button_width // 2, start_y,
                   button_width, button_height, "Try Again", GREEN, LIGHT_GRAY),
            Button(center_x - button_width // 2, start_y + button_height + button_spacing,
                   button_width, button_height, "Main Menu", BLUE, LIGHT_GRAY),
            Button(center_x - button_width // 2, start_y + 2 * (button_height + button_spacing),
                   button_width, button_height, "Quit", RED, LIGHT_GRAY)
        ]

    def _create_leaderboard_menu(self):
        button_width = 200
        button_height = 50
        self.leaderboard_buttons = [
            Button(self.width // 2 - button_width // 2, self.height - button_height - 30,
                   button_width, button_height, "Back", BLUE, LIGHT_GRAY)
        ]

    def _create_hud(self):
        self.health_bar = ProgressBar(20, 20, 200, 20, 100, 100, GREEN)

    def add_score(self, name, score):
        # under construction
        pass

    def _load_leaderboard(self):
        # under construction
        return []

    def _save_leaderboard(self):
        # under construction
        pass

    def update(self, mouse_pos, mouse_clicked, keys_pressed):
        
        action = None

        if self.state == STATE_GAME and keys_pressed[pygame.K_ESCAPE]:
            self.state = STATE_PAUSED
            action = 'pause'

        if self.state == STATE_MAIN_MENU:
            for button in self.main_menu_buttons:
                button.update(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Start Game":
                        self.state = STATE_GAME
                        action = 'start'
                    elif button.text == "Leaderboard":
                        self.state = STATE_LEADERBOARD
                    elif button.text == "Quit":
                        action = 'quit'

        elif self.state == STATE_PAUSED:
            for button in self.pause_menu_buttons:
                button.update(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Resume":
                        self.state = STATE_GAME
                        action = 'resume'
                    elif button.text == "Main Menu":
                        self.state = STATE_MAIN_MENU
                        action = 'main_menu'
                    elif button.text == "Quit":
                        action = 'quit'

        elif self.state == STATE_GAME_OVER:
            for button in self.game_over_buttons:
                button.update(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Try Again":
                        self.state = STATE_GAME
                        action = 'restart'
                    elif button.text == "Main Menu":
                        self.state = STATE_MAIN_MENU
                        action = 'main_menu'
                    elif button.text == "Quit":
                        action = 'quit'

        elif self.state == STATE_LEADERBOARD:
            for button in self.leaderboard_buttons:
                button.update(mouse_pos)
                if mouse_clicked and button.is_clicked(mouse_pos, mouse_clicked):
                    if button.text == "Back":
                        self.state = STATE_MAIN_MENU
        self.health_bar.update(self.player_health)
        return self.state, action

    def set_player_health(self, health):
        self.player_health = health

    def set_score(self, score):
        self.score = score
        if score > self.high_score:
            self.high_score = score

    def game_over(self):
        self.state = STATE_GAME_OVER

    def draw(self, screen):
        """This is a note to fix this part to be more clear"""
        if self.state == STATE_MAIN_MENU:
            screen.fill(BLACK)
            title_text = FONT_LARGE.render("SPACE SHOOTER", True, WHITE)
            title_rect = title_text.get_rect(
                center=(self.width // 2, self.height // 4))
            screen.blit(title_text, title_rect)

            for button in self.main_menu_buttons:
                button.draw(screen)

        elif self.state == STATE_GAME:
            health_text = FONT_SMALL.render("HEALTH", True, WHITE)
            screen.blit(health_text, (20, 5))
            self.health_bar.draw(screen)

            score_text = FONT_MEDIUM.render(
                f"SCORE: {self.score}", True, WHITE)
            screen.blit(score_text, (self.width -
                        score_text.get_width() - 20, 20))
            high_score_text = FONT_SMALL.render(
                f"HIGH SCORE: {self.high_score}", True, LIGHT_GRAY)
            screen.blit(high_score_text, (self.width -
                        high_score_text.get_width() - 20, 50))

        elif self.state == STATE_PAUSED:
            overlay = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            pause_text = FONT_LARGE.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(
                center=(self.width // 2, self.height // 4))
            screen.blit(pause_text, pause_rect)

            for button in self.pause_menu_buttons:
                button.draw(screen)

        elif self.state == STATE_GAME_OVER:
            overlay = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            game_over_text = FONT_LARGE.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(
                center=(self.width // 2, self.height // 4))
            screen.blit(game_over_text, game_over_rect)

            score_text = FONT_MEDIUM.render(
                f"FINAL SCORE: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(
                center=(self.width // 2, self.height // 3))
            screen.blit(score_text, score_rect)

            for button in self.game_over_buttons:
                button.draw(screen)

        elif self.state == STATE_LEADERBOARD:
            screen.fill(BLACK)
            title_text = FONT_LARGE.render("LEADERBOARD", True, WHITE)
            title_rect = title_text.get_rect(center=(self.width // 2, 50))
            screen.blit(title_text, title_rect)

            no_scores_text = FONT_MEDIUM.render(
                "Leaderboard under construction", True, LIGHT_GRAY)
            no_scores_rect = no_scores_text.get_rect(
                center=(self.width // 2, self.height // 2))
            screen.blit(no_scores_text, no_scores_rect)

            for button in self.leaderboard_buttons:
                button.draw(screen)
