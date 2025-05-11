"""module to manage high scores for the game."""
import json
import os


class HighScoreManager:
    """Manages loading, saving, and displaying high scores."""

    def __init__(self, filename="high_scores.json"):
        self.filename = filename
        self.high_scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_scores(self):
        with open(self.filename, 'w') as f:
            json.dump(self.high_scores, f)

    def add_score(self, score):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]  # only top 10
        self.save_scores()

    def get_top_scores(self, limit=10):
        return self.high_scores[:limit]
