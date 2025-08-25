import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from src.hlogic import HangmanLogic

class HangmanGUI:
    def __init__(self, master, word_list):
        self.master = master
        self.word_list = word_list
        self.level_var = tk.StringVar(value="basic")

        # Set up the main window.
        self.master.title("Hangman")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        self.master.configure(bg="#f8f9fa")
        self.master.option_add("*Font", "Arial 10")

        # Bind keyboard input.
        self.master.bind("<Key>", self.handle_keypress)

        # Create level selection screen.
        self.create_level_selection()

    def create_level_selection(self):
        title_label = tk.Label(
            self.master,
            text="Hangman",
            font=("Arial", 20, "bold"),
            bg="#f8f9fa",
            fg="darkblue"
        )
        title_label.pack(pady=40)

        level_label = tk.Label(
            self.master,
            text="Select Level:",
            font=("Arial", 14, "bold"),
            bg="#f8f9fa",
            fg="black"
        )
        level_label.pack(pady=10)

        levels = ["basic", "intermediate"]
        self.level_menu = tk.OptionMenu(self.master, self.level_var, *levels)
        self.level_menu.config(
            font=("Arial", 12),
            bg="#ffffff",
            fg="black",
            relief="raised",
            borderwidth=2,
            width=12
        )
        self.level_menu.pack(pady=10)

        self.start_button = tk.Button(
            self.master,
            text="Start Game",
            command=self.start_game,
            font=("Arial", 12, "bold"),
            bg="#28a745",
            fg="white",
            relief="raised",
            borderwidth=2,
            padx=20,
            pady=10,
            activebackground="#218838"
        )
        self.start_button.pack(pady=20)

        note_label = tk.Label(
            self.master,
            text="Note: You can use the Keyboard!",
            font=("Arial", 10),
            bg="#f8f9fa",
            fg="gray"
        )
        note_label.pack(pady=10)

    def start_game(self):
        self.level = self.level_var.get()

        # Hide level selection widgets.
        for widget in self.master.winfo_children():
            widget.destroy()

        # Initialize game logic.
        self.game = HangmanLogic(self.word_list, self.level)

        # Load images for hangman states (optional).
        self.image_path = [f"images/hangman{i}.png" for i in range(6, -1, -1)]
        try:
            self.images = [ImageTk.PhotoImage(Image.open(p).resize((200, 200))) for p in self.image_path]
        except Exception:
            self.images = [None] * 7  # Fallback if images are missing.

        # Create in-game widgets.
        self.create_widgets()
        self.update_display()
        self.start_timer()

    def create_widgets(self):
        status_frame = tk.Frame(self.master, bg="#f8f9fa")
        status_frame.place(x=0, y=0, width=600, height=40)

        self.timer_label = tk.Label(
            status_frame,
            text="Time left: 15s",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="red"
        )
        self.timer_label.place(x=10, y=5)

        self.level_label_game = tk.Label(
            status_frame,
            text=f"Level: {self.level.capitalize()}",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="darkblue"
        )
        self.level_label_game.place(x=150, y=5)

        self.lives = tk.Label(
            status_frame,
            text=f"Tries left: {self.game.tries}",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="darkred"
        )
        self.lives.place(x=300, y=5)

        self.score_status = tk.Label(
            status_frame,
            text=f"Score: {self.game.score}",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="green"
        )
        self.score_status.place(x=450, y=5)

        # Hangman image panel.
        self.panel = tk.Label(self.master, bg="#f8f9fa")
        self.panel.place(x=50, y=60)

        self.word_display = tk.Label(
            self.master,
            font=("Arial", 20, "bold"),
            bg="#f8f9fa",
            fg="darkblue"
        )
        self.word_display.place(x=270, y=160)

        self.buttons = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            row = 300 + (i // 13) * 40
            col = 50 + (i % 13) * 40
            btn = tk.Button(
                self.master,
                text=letter,
                width=3,
                height=1,
                font=("Arial", 12),
                bg="#f0f0f0",
                fg="black",
                activebackground="#e0e0e0",
                relief="raised",
                borderwidth=1,
                command=lambda l=letter: self.make_guess(l),
            )
            btn.place(x=col, y=row)
            self.buttons[letter] = btn

    def make_guess(self, letter):
        result = self.process_guess(letter)
        if result == "win":
            self.check_game_over("You won!")
        elif result == "lose":
            self.check_game_over(f"You lose! Correct word: {self.game.hidden_word}")

    def handle_keypress(self, event):
        if not hasattr(self, "game") or self.game.game_over:
            return

        key = event.char.upper()
        if key.isalpha() and len(key) == 1:
            result = self.process_guess(key)
            if result == "win":
                self.check_game_over("You won!")
            elif result == "lose":
                self.check_game_over(f"You lose! Correct word: {self.game.hidden_word}")

    def process_guess(self, letter):
        if letter in self.buttons:
            self.buttons[letter].configure(state="disabled")

        result = self.game.guess(letter)
        self.update_display()
        self.time_left = 15  # Reset timer after a guess.
        return result

    def start_timer(self):
        self.time_left = 15
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        if self.time_left > 0 and not self.game.game_over:
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        elif not self.game.game_over:
            self.game.tries -= 1
            self.lives.config(text=f"Tries left: {self.game.tries}")
            self.update_display()
            if self.game.tries == 0:
                self.check_game_over("Time's up! No tries left!")
            else:
                self.time_left = 15
                self.update_timer()

    def update_display(self):
        self.word_display.config(text=" ".join(self.game.guess_word))
        self.score_status.config(text=f"Score: {self.game.score}")
        self.lives.config(text=f"Tries left: {self.game.tries}")
        if self.images[self.game.tries]:
            self.panel.config(image=self.images[self.game.tries])
            self.panel.image = self.images[self.game.tries]

    def check_game_over(self, msg):
        self.game.game_over = True
        for btn in self.buttons.values():
            btn.config(state="disabled")

        messagebox.showinfo("Game Over", msg)

        if hasattr(self, 'new_game_btn'):
            self.new_game_btn.destroy()

        self.new_game_btn = tk.Button(
            self.master,
            text="New Game",
            font=("Arial", 12, "bold"),
            bg="#007bff",
            fg="white",
            relief="raised",
            borderwidth=2,
            command=self.new_game,
        )
        self.new_game_btn.place(x=250, y=400)

    def new_game(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_level_selection()