
import numpy as np

EMPTY, BLACK, WHITE = 0, 1, -1
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),         (0, 1),
              (1, -1),  (1, 0), (1, 1)]

class Board:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3] = WHITE
        self.board[3, 4] = BLACK
        self.board[4, 3] = BLACK
        self.board[4, 4] = WHITE

    def display(self):
        print("  " + " ".join(str(i) for i in range(8)))
        for i in range(8):
            row = []
            for j in range(8):
                piece = self.board[i][j]
                if piece == BLACK:
                    row.append('B')
                elif piece == WHITE:
                    row.append('W')
                else:
                    row.append('.')
            print(i, " ".join(row))

    def is_on_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def get_valid_moves(self, player):
        moves = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == EMPTY and self.is_valid_move(player, x, y):
                    moves.append((x, y))
        return moves

    def is_valid_move(self, player, x_start, y_start):
        if self.board[x_start][y_start] != EMPTY or not self.is_on_board(x_start, y_start):
            return False

        opponent = -player
        for dx, dy in DIRECTIONS:
            x, y = x_start + dx, y_start + dy
            has_opponent = False
            while self.is_on_board(x, y) and self.board[x][y] == opponent:
                x += dx
                y += dy
                has_opponent = True
            if has_opponent and self.is_on_board(x, y) and self.board[x][y] == player:
                return True
        return False

    def make_move(self, player, x_start, y_start):
        if not self.is_valid_move(player, x_start, y_start):
            return False

        self.board[x_start][y_start] = player
        opponent = -player

        for dx, dy in DIRECTIONS:
            x, y = x_start + dx, y_start + dy
            pieces_to_flip = []
            while self.is_on_board(x, y) and self.board[x][y] == opponent:
                pieces_to_flip.append((x, y))
                x += dx
                y += dy
            if self.is_on_board(x, y) and self.board[x][y] == player:
                for x_flip, y_flip in pieces_to_flip:
                    self.board[x_flip][y_flip] = player
        return True

    def is_game_over(self):
        return not (self.get_valid_moves(BLACK) or self.get_valid_moves(WHITE))

    def get_score(self):
        black_score = np.sum(self.board == BLACK)
        white_score = np.sum(self.board == WHITE)
        return black_score, white_score
