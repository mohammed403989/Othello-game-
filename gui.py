import tkinter as tk
from tkinter import messagebox
from board import Board
from minimax import get_best_move

TILE_SIZE = 60
BOARD_SIZE = 8

class OthelloApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello Game")

        self.intro_frame = tk.Frame(master, bg="lightblue")
        self.intro_frame.pack(fill="both", expand=True)

        tk.Label(self.intro_frame, text="Welcome to Othello!", font=("Arial", 22), bg="lightblue").pack(pady=30)
        tk.Button(self.intro_frame, text="Start Game", command=self.show_mode_selection, font=("Arial", 16)).pack(pady=10)
        tk.Button(self.intro_frame, text="Exit", command=master.quit, font=("Arial", 14)).pack(pady=10)

    def show_mode_selection(self):
        self.intro_frame.destroy()

        self.mode_frame = tk.Frame(self.master, bg="lightyellow")
        self.mode_frame.pack(fill="both", expand=True)

        tk.Label(self.mode_frame, text="Choose Game Mode:", font=("Arial", 16), bg="lightyellow").pack(pady=10)

        tk.Label(self.mode_frame, text="AI Difficulty (1-5):", font=("Arial", 12), bg="lightyellow").pack(pady=5)
        self.difficulty_var = tk.IntVar(value=3)
        tk.Spinbox(self.mode_frame, from_=1, to=5, textvariable=self.difficulty_var, font=("Arial", 12)).pack(pady=5)

        tk.Button(self.mode_frame, text="Play Against Computer", font=("Arial", 14),
                  command=lambda: self.start_game(vs_computer=True)).pack(pady=10)

        tk.Button(self.mode_frame, text="Play Against Friend", font=("Arial", 14),
                  command=lambda: self.start_game(vs_computer=False)).pack(pady=10)

    def start_game(self, vs_computer):
        self.mode_frame.destroy()
        OthelloGUI(self.master, vs_computer=vs_computer, difficulty=self.difficulty_var.get())

class OthelloGUI:
    def __init__(self, master, vs_computer=True, difficulty=3):
        self.master = master
        self.vs_computer = vs_computer
        self.difficulty = difficulty
        self.board = Board()
        self.current_player = 1

        self.score_label = tk.Label(master, text="", font=('Arial', 14))
        self.score_label.pack()

        self.canvas = tk.Canvas(master, width=TILE_SIZE*BOARD_SIZE, height=TILE_SIZE*BOARD_SIZE, bg='green')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_handler)

        self.quit_button = tk.Button(master, text="End Game", font=('Arial', 12), command=self.show_winner)
        self.quit_button.pack(pady=5)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        black_score, white_score = self.board.get_score()
        self.score_label.config(text=f"Black: {black_score} | White: {white_score}")

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * TILE_SIZE
                y1 = row * TILE_SIZE
                x2 = x1 + TILE_SIZE
                y2 = y1 + TILE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                piece = self.board.board[row][col]
                if piece != 0:
                    color = "black" if piece == 1 else "white"
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color)

    def click_handler(self, event):
        col = event.x // TILE_SIZE
        row = event.y // TILE_SIZE
        if self.board.is_valid_move(self.current_player, row, col):
            self.board.make_move(self.current_player, row, col)
            self.current_player *= -1
            self.draw_board()
            if self.board.is_game_over():
                self.show_winner()
            elif self.vs_computer and self.current_player == -1:
                self.master.after(500, self.ai_move)

    def ai_move(self):
        move = get_best_move(self.board, self.current_player, depth=self.difficulty)
        if move:
            self.board.make_move(self.current_player, move[0], move[1])
            self.current_player *= -1
        self.draw_board()
        if self.board.is_game_over():
            self.show_winner()

    def show_winner(self):
        black_score, white_score = self.board.get_score()
        self.canvas.destroy()
        self.score_label.destroy()
        self.quit_button.destroy()
        msg = ""
        if black_score > white_score:
            msg = "Victory sealed — and you're the undisputed champion! 👑🔥"
        elif white_score > black_score:
            msg = "Game Over : Looks like your intelligence went on vacation today! 🤦‍♀🎲"
        else:
            msg = "A draw? Looks like you got into the AI's head and left it confused! 🤖"

        end_frame = tk.Frame(self.master, bg="lightblue")
        end_frame.pack(fill="both", expand=True)

        label = tk.Label(end_frame, text=msg, font=("Arial", 18), bg="lightblue", wraplength=500, justify="center")
        label.pack(pady=50)

        restart_btn = tk.Button(end_frame, text="Play Again", font=("Arial", 14), command=self.restart_game)
        restart_btn.pack(pady=10)

        exit_btn = tk.Button(end_frame, text="Exit Game", font=("Arial", 14), command=self.master.quit)
        exit_btn.pack(pady=10)

    def restart_game(self):
        self.master.destroy()
        root = tk.Tk()
        app = OthelloApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = OthelloApp(root)
    root.mainloop()

