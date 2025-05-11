"""Testing for the HighScoreManager class."""
import unittest
import os
from highscore import HighScoreManager


class TestHighScoreManager(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_high_scores.json"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        self.manager = HighScoreManager(self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_initialization(self):
        self.assertEqual(self.manager.high_scores, [])

    def test_add_score(self):
        self.manager.add_score(100)
        self.assertEqual(self.manager.high_scores, [100])

    def test_score_sorting(self):
        scores = [50, 200, 100, 150]
        for score in scores:
            self.manager.add_score(score)
        self.assertEqual(self.manager.high_scores, [200, 150, 100, 50])

    def test_top_10_limitation(self):
        for i in range(15):
            self.manager.add_score(i * 10)
        self.assertEqual(len(self.manager.high_scores), 10)
        self.assertEqual(self.manager.high_scores[0], 140)

    def test_save_and_load(self):
        self.manager.add_score(300)
        self.manager.add_score(200)
        self.manager.save_scores()

        new_manager = HighScoreManager(self.test_filename)
        self.assertEqual(new_manager.high_scores, [300, 200])


if __name__ == "__main__":
    unittest.main()
