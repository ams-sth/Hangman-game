import tkinter as tk
from src.hgui import HangmanGUI

if __name__ == "__main__":
    word_list = [
        "CAT", "BEAR", "LION", "COMPUTER", "CHINA", "NEPAL", "DENMARK",
        "HEN", "DOVE", "CRANE", "NAME", "PLACE", "FAST", "SLOW",
        "KING", "THOR", "KRATOS", "DANTE", "VIDEO", "MUSIC"
    ]

    root = tk.Tk()
    game = HangmanGUI(root, word_list)
    root.mainloop()