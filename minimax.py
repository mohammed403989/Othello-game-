import copy

def get_valid_moves(board, player):
    return board.get_valid_moves(player)

def minimax(board, depth, maximizing_player, player):
    valid_moves = get_valid_moves(board, player)
    if depth == 0 or not valid_moves:
        return board.get_score()[player], None

    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move[0], move[1], player)
            eval_score, _ = minimax(new_board, depth - 1, False, -player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move[0], move[1], player)
            eval_score, _ = minimax(new_board, depth - 1, True, -player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

def get_best_move(board, player, depth=2):
    _, move = minimax(board, depth, True, player)
    return move
