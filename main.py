
from board import Board, BLACK, WHITE
from player import HumanPlayer, AIPlayer

def play_game():
    board = Board()
    player1 = HumanPlayer(BLACK)
    player2 = AIPlayer(WHITE, depth=3)
    current_player = player1

    while not board.is_game_over():
        board.display()
        moves = board.get_valid_moves(current_player.color)
        if moves:
            print(f"Player {'B' if current_player.color == BLACK else 'W'}'s turn")
            move = current_player.get_move(board)
            board.make_move(current_player.color, *move)
        current_player = player2 if current_player == player1 else player1

    board.display()
    black_score, white_score = board.get_score()
    print(f"Game Over! Score - Black: {black_score}, White: {white_score}")

if __name__ == "__main__":
    play_game()
