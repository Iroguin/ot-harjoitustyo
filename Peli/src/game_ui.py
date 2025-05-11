"""UI for game."""
from enum import Enum, auto
import pygame
from highscore import HighScoreManager

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

FONT_SMALL = FONT_MEDIUM = FONT_LARGE = None


class GameState(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    LEADERBOARD = auto()


class Button:
    """A clickable button for the UI."""

    def __init__(self, rect, text, color=LIGHT_GRAY):
        hover_color = WHITE
        text_color = BLACK
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        bg = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, bg, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        text_surf = FONT_MEDIUM.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos, mouse_click=False):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered and mouse_click

    def set_color(self, color):
        self.color = color

    def set_text(self, text):
        self.text = text

    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click


class ProgressBar:
    """A bar UI element for displaying values like health."""

    def __init__(self, rect, value=100, max_value=100):
        color = GREEN
        background = GRAY
        self.rect = pygame.Rect(rect)
        self.value = value
        self.max_value = max_value
        self.color = color
        self.background = background

    def update(self, new_value):
        self.value = max(0, min(new_value, self.max_value))

    def draw(self, screen):
        pygame.draw.rect(screen, self.background, self.rect, border_radius=3)
        if self.value:
            fill_width = int(self.rect.width * (self.value / self.max_value))
            fill_rect = pygame.Rect(
                self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, self.color, fill_rect, border_radius=3)
        pygame.draw.rect(screen, BLACK, self.rect, 1, border_radius=3)


class GameUI:
    """Class for managing game UI states and rendering."""
    BUTTON_CONFIG = {
        GameState.MAIN_MENU: ["Start Game", "Leaderboard", "Quit"],
        GameState.PAUSED: ["Resume", "Main Menu", "Quit"],
        GameState.GAME_OVER: ["Try Again", "Main Menu", "Quit"],
        GameState.LEADERBOARD: ["Back"],
    }

    def __init__(self, screen_width, screen_height):
        pygame.font.init()
        global FONT_SMALL, FONT_MEDIUM, FONT_LARGE
        FONT_SMALL = pygame.font.SysFont("Arial", 16)
        FONT_MEDIUM = pygame.font.SysFont("Arial", 24)
        FONT_LARGE = pygame.font.SysFont("Arial", 48)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = GameState.MAIN_MENU
        self.score = self.high_score = 0
        self.player_health = 100

        self.high_score_manager = HighScoreManager()

        self.menus = self._create_menus()
        self.health_bar = ProgressBar((20, 20, 200, 20))

    def _create_menus(self):
        menus = {}
        center_x = self.screen_width // 2
        for state, texts in self.BUTTON_CONFIG.items():
            buttons = []
            count = len(texts)
            total_height = count * 50 + (count - 1) * 20
            start_y = (self.screen_height - total_height) // 2
            for i, text in enumerate(texts):
                x = center_x - 100
                y = start_y + i * 70
                color = {"Quit": RED, "Resume": GREEN,
                         "Try Again": GREEN}.get(text, BLUE)
                buttons.append(Button((x, y, 200, 50), text, color))
            menus[state] = buttons
        return menus

    def update(self, mouse_pos, mouse_click, keys_pressed):
        action = None
        if self.state == GameState.GAME and keys_pressed[pygame.K_ESCAPE]:
            self.state = GameState.PAUSED
            return self.state, 'pause'

        for button in self.menus.get(self.state, []):
            if button.update(mouse_pos, mouse_click):
                action = self._handle_button(button.text)
                break

        # update health
        self.health_bar.update(self.player_health)
        return self.state, action

    def _handle_button(self, text):
        transitions = {
            "Start Game": (GameState.GAME, 'start'),
            "Leaderboard": (GameState.LEADERBOARD, None),
            "Quit": (None, 'quit'),
            "Resume": (GameState.GAME, 'resume'),
            "Main Menu": (GameState.MAIN_MENU, 'main_menu'),
            "Try Again": (GameState.GAME, 'restart'),
            "Back": (GameState.MAIN_MENU, None),
        }
        new_state, action = transitions.get(text, (None, None))
        if new_state:
            self.state = new_state
        return action

    def set_player_health(self, health):
        self.player_health = health

    def set_score(self, score):
        self.score = score
        self.high_score = max(self.high_score, score)

    def game_over(self):
        self.high_score_manager.add_score(self.score)
        self.state = GameState.GAME_OVER

    def draw(self, screen):
        if self.state in [GameState.PAUSED, GameState.GAME_OVER]:
            overlay = pygame.Surface(
                (self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

        titles = {
            GameState.MAIN_MENU: "SPACE SHOOTER",
            GameState.PAUSED: "PAUSED",
            GameState.GAME_OVER: "GAME OVER",
            GameState.LEADERBOARD: "LEADERBOARD",
        }
        title = titles.get(self.state)
        if title:
            color = RED if self.state == GameState.GAME_OVER else WHITE
            text_surf = FONT_LARGE.render(title, True, color)
            rect = text_surf.get_rect(
                center=(self.screen_width//2, self.screen_height//4))
            screen.blit(text_surf, rect)

        # HUD
        if self.state == GameState.GAME:
            screen.blit(FONT_SMALL.render("HEALTH", True, WHITE), (20, 5))
            self.health_bar.draw(screen)
            score_surf = FONT_MEDIUM.render(
                f"SCORE: {self.score}", True, WHITE)
            screen.blit(score_surf, (self.screen_width -
                        score_surf.get_width() - 20, 20))
            hs_surf = FONT_SMALL.render(
                f"HIGH SCORE: {self.high_score}", True, LIGHT_GRAY)
            screen.blit(hs_surf, (self.screen_width -
                        hs_surf.get_width() - 20, 50))

        if self.state == GameState.LEADERBOARD:
            self._draw_leaderboard(screen)

        # buttons
        for button in self.menus.get(self.state, []):
            button.draw(screen)

    def _draw_leaderboard(self, screen):
        top_scores = self.high_score_manager.get_top_scores(10)
        start_y = self.screen_height // 3
        line_height = 40
        rank_x = self.screen_width // 3
        score_x = self.screen_width * 2 // 3
        pygame.draw.line(screen, WHITE,
                         (self.screen_width//3 - 50, start_y - line_height//2),
                         (self.screen_width*2//3 + 50, start_y - line_height//2), 2)

        for i, score in enumerate(top_scores):
            y = start_y + i * line_height
            rank_surf = FONT_MEDIUM.render(f"#{i+1}", True, WHITE)
            rank_rect = rank_surf.get_rect(center=(rank_x, y))
            screen.blit(rank_surf, rank_rect)
            score_surf = FONT_MEDIUM.render(str(score), True, WHITE)
            score_rect = score_surf.get_rect(center=(score_x, y))
            screen.blit(score_surf, score_rect)


# compatibility
STATE_MAIN_MENU = GameState.MAIN_MENU
STATE_GAME = GameState.GAME
STATE_PAUSED = GameState.PAUSED
STATE_GAME_OVER = GameState.GAME_OVER
STATE_LEADERBOARD = GameState.LEADERBOARD
