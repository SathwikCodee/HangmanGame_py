from tkinter import *
from tkinter import messagebox
import random
from hangman_words import word_list
from PIL import Image, ImageTk, ImageFilter


class HangmanGame:

    def __init__(self, window):

        self.blurred_image = None
        self.bg_image = None
        self.resized_bg_image = None
        self.original_bg_image = None
        self.background_set = None
        self.head_text = None
        self.canvas = None
        self.word_label = None
        self.entry_label = None
        self.entry = None
        self.guess_button = None
        self.window = window
        self.window.title("Hangman Game")
        self.window.geometry("1000x750")  # height x width
        self.word = random.choice(word_list)
        self.guessed_letters = set()
        self.attempts = 6
        self.create_widgets()

    def create_widgets(self):

        self.bg_image = Image.open("logo.png")
        self.resized_bg_image = self.bg_image.resize((1000, 750), Image.LANCZOS)
        self.blurred_image = self.resized_bg_image.filter(ImageFilter.GaussianBlur(radius=8))
        self.original_bg_image = (ImageTk.PhotoImage(self.blurred_image))

        self.background_set = Label(self.window, image=self.original_bg_image, bg='black')
        self.background_set.place(relheight=1, relwidth=1)

        self.head_text = Label(self.window, text="HANGMAN", fg='orange', font="Times 40 italic bold underline",
                               bg='black')
        self.head_text.pack(pady=10)

        self.canvas = Canvas(self.window, width=500, height=300, bg='black')
        self.canvas.pack(pady=20)

        self.word_label = Label(self.window, text=self.get_display_word(), font=('Times 40 italic', 25), bg='green',
                                padx=20, pady=10)
        self.word_label.pack(pady=20)

        self.entry_label = Label(self.window, text="Enter a letter : ", font=('Palatine Linotype', 17), bg='green'
                                 , padx=5, pady=5)
        self.entry_label.pack(pady=10)

        self.entry = Entry(self.window, font=('Palatine Linotype', 14))
        self.entry.pack(pady=10)

        self.guess_button = Button(self.window, text="Guess", command=self.make_guess, font=('Helvetica', 14),
                                   bg='green', fg='white', border=0, cursor='hand2')
        self.guess_button.pack(pady=10)

        self.draw_hangman()

    def make_guess(self):
        guess = self.entry.get().upper()
        self.entry.delete(0, END)

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showwarning("Invalid input", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Duplicate guess", "You have already guessed that letter.")
            return

        self.guessed_letters.add(guess)

        if guess not in self.word:
            self.attempts -= 1
        self.update_game_state()

    def update_game_state(self):
        self.word_label.config(text=self.get_display_word())
        self.draw_hangman()
        if '_' not in self.get_display_word():
            messagebox.showinfo("Congratulations", "You won! The word was " + self.word)
            self.window.quit()
        if self.attempts == 0:
            messagebox.showinfo("Game Over", "You lost! The word was " + self.word)
            self.window.quit()

    def get_display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def draw_hangman(self):
        self.canvas.delete("all")
        # Drawing the hangman base and parts based on attempts left
        if self.attempts <= 5:
            self.canvas.create_line(150, 200, 350, 200, width=5, fil="white")  # Base
            self.canvas.create_line(200, 200, 200, 50, width=5, fil="white")  # Vertical pole
            self.canvas.create_line(200, 50, 300, 50, width=5, fil="white")  # Top horizontal pole
        if self.attempts <= 4:
            self.canvas.create_line(300, 50, 300, 80, width=5, fil="white")  # Rope
        if self.attempts <= 3:
            self.canvas.create_oval(280, 80, 320, 120, width=8, fil="orange")  # Head
        if self.attempts <= 2:
            self.canvas.create_line(300, 120, 300, 170, width=5, fil="orange")  # Body
        if self.attempts <= 1:
            self.canvas.create_line(300, 130, 280, 150, width=5, fil="orange")  # Left arm
            self.canvas.create_line(300, 130, 320, 150, width=5, fil="orange")  # Right arm
        if self.attempts == 0:
            self.canvas.create_line(300, 170, 280, 190, width=5, fil="orange")  # Left leg
            self.canvas.create_line(300, 170, 320, 190, width=5, fil="orange")  # Right leg


if __name__ == "__main__":
    window = Tk()
    game = HangmanGame(window)
    window.mainloop()
