import random
import string
import nltk
from nltk.corpus import brown

# Ensure NLTK resources are downloaded
nltk.download('brown')

class HangmanLogic:
    def __init__(self, word_list, level="basic", dictionary_path="src\dictionary.txt"):
        try:
            with open(dictionary_path, "r") as f:
                self.dictionary = set(line.strip().upper() for line in f)
        except FileNotFoundError:
            raise FileNotFoundError("Dictionary file not found. Please provide a valid dictionary path.")

        self.level = level

        # Filter word list to include only valid words
        self.word_list = [w.upper() for w in word_list if w.upper() in self.dictionary]
        if not self.word_list:
            raise ValueError("Word list must contain valid words.")

        # Generate random phrases dynamically for intermediate level
        if self.level == "intermediate":
            self.phrase_list = self.generate_random_phrases()
        else:
            self.phrase_list = []

        self.reset()

    def generate_random_phrases(self):
        """Generate random phrases from the Brown corpus."""
        phrases = []
        for sentence in brown.sents():
            phrase = " ".join(sentence).upper()
            if 2 <= len(phrase.split()) <= 5:  # Limit phrase length
                phrases.append(phrase)
            if len(phrases) >= 10:  # Limit number of phrases
                break
        return phrases

    def reset(self):
        if self.level == "basic":
            self.hidden_word = random.choice(self.word_list).upper()
        else:
            self.hidden_word = random.choice(self.phrase_list).upper()

        self.current_display_word = ["_" if c != " " else " " for c in self.hidden_word]
        self.tries = 6
        self.score = 0
        self.game_over = False
        self.guessed_letters = set()

    @property
    def guess_word(self):
        return self.current_display_word

    def guess(self, letter):
        if self.game_over:
            return None

        if not letter or len(letter) != 1 or letter.upper() not in string.ascii_uppercase:
            return "invalid"

        letter = letter.upper()
        if letter in self.guessed_letters:
            return "already"

        self.guessed_letters.add(letter)

        if letter in self.hidden_word:
            for i, c in enumerate(self.hidden_word):
                if c == letter:
                    self.current_display_word[i] = letter
                    self.score += 1
            if "_" not in self.current_display_word:
                self.game_over = True
                return "win"
            return "correct"
        else:
            self.tries -= 1
            if self.tries <= 0:
                self.game_over = True
                return "lose"
            return "wrong"