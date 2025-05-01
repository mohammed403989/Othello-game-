
from minimax import minimax

class HumanPlayer:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        while True:
            try:
                x, y = map(int, input("Enter move (row col): ").split())
                if (x, y) in board.get_valid_moves(self.color):
                    return x, y
                else:
                    print("Invalid move.")
            except:
                print("Invalid input. Try again.")

class AIPlayer:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def get_move(self, board):
        _, move = minimax(board, self.depth, True, self.color)
        return move
