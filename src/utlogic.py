import unittest
from src.hlogic import HangmanLogic

class TestHangmanLogic(unittest.TestCase):

    def setUp(self):
        self.dictionary_path = "src/dictionary.txt"
        self.game_basic = HangmanLogic(level="basic", dictionary_path=self.dictionary_path)
        self.game_intermediate = HangmanLogic(level="intermediate", dictionary_path=self.dictionary_path)

    def test_initial_state(self):
        for game in [self.game_basic, self.game_intermediate]:
            self.assertEqual(game.tries, 6)
            self.assertEqual(game.score, 0)
            self.assertFalse(game.game_over)
            self.assertIn("_", game.current_display_word)

    def test_correct_guess(self):
        letter = self.game_basic.hidden_word[0]
        result = self.game_basic.guess(letter)
        self.assertIn(letter, self.game_basic.guessed_letters)
        self.assertIn(letter, self.game_basic.current_display_word)
        self.assertIn(result, ["correct", "win"])

    def test_wrong_guess(self):
        letter = "Z"
        while letter in self.game_basic.hidden_word:
            letter = chr(ord(letter) - 1)
        tries_before = self.game_basic.tries
        result = self.game_basic.guess(letter)
        self.assertEqual(result, "wrong")
        self.assertEqual(self.game_basic.tries, tries_before - 1)

    def test_win_condition(self):
        for letter in set(self.game_basic.hidden_word):
            self.game_basic.guess(letter)
        self.assertTrue(self.game_basic.game_over)
        self.assertNotIn("_", self.game_basic.current_display_word)

    def test_lose_condition(self):
        wrong_letters = [chr(i) for i in range(65, 91) if chr(i) not in self.game_basic.hidden_word]
        for i in range(6):
            self.game_basic.guess(wrong_letters[i])
        self.assertTrue(self.game_basic.game_over)
        self.assertEqual(self.game_basic.tries, 0)
        self.assertIsNone(self.game_basic.guess("X"))

    def test_reset_functionality(self):
        self.game_basic.guess("A")
        self.game_basic.guess("B")
        self.game_basic.reset()
        self.assertEqual(self.game_basic.tries, 6)
        self.assertEqual(self.game_basic.score, 0)
        self.assertFalse(self.game_basic.game_over)
        self.assertEqual(len(self.game_basic.guessed_letters), 0)
        self.assertIn("_", self.game_basic.guess_word)
        self.assertNotEqual(self.game_basic.hidden_word, "")

    def test_intermediate_phrase(self):
        self.game_intermediate.reset()
        self.assertIn(" ", self.game_intermediate.hidden_word)
        self.assertTrue(len(self.game_intermediate.hidden_word.split()) >= 2)

    def test_invalid_input(self):
        for val in ["", "AB", "1", "!", "@"]:
            self.assertEqual(self.game_basic.guess(val), "invalid")

    def test_repeated_guess(self):
        letter = self.game_basic.hidden_word[0]
        self.game_basic.guess(letter)
        self.assertEqual(self.game_basic.guess(letter), "already")

if __name__ == "__main__":
    unittest.main()
   