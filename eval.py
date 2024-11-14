import chess
import random

def get_random_moves(board):
    first_moves = [m for m in board.legal_moves if check_first(board, m)]
    last_moves = [m for m in board.legal_moves if not check_first(board, m)]
    random.shuffle(first_moves)
    random.shuffle(last_moves)
    # print(len(first_moves), len(last_moves))
    return first_moves, last_moves

def get_color(board):
    # return the color that just played
    # return white: 1 black: -1
    return ((len(board.move_stack) % 2) * 2 - 1)

def score_board(board):
    """
    returns evaluation [-1, 1]
    black wants -1
    white wants 1
    """
    if board.can_claim_draw() or board.can_claim_fifty_moves() or board.can_claim_threefold_repetition() or board.is_stalemate():
        # print("draw")
        return 0
    if board.is_checkmate():
        # print("checkmate")
        return get_color(board)
    else:
        # print("material advantage")
        white_material = len(
            board.pieces(chess.PAWN, chess.WHITE)
        ) * 1 + len(
            board.pieces(chess.KNIGHT, chess.WHITE)
        ) * 3 + len(
            board.pieces(chess.BISHOP, chess.WHITE)
        ) * 3 + len(
            board.pieces(chess.ROOK, chess.WHITE)
        ) * 5 + len(
            board.pieces(chess.QUEEN, chess.WHITE)
        ) * 9 + len(
            board.pieces(chess.KING, chess.WHITE)
        ) * 1
        
        black_material = len(
            board.pieces(chess.PAWN, chess.BLACK)
        ) * 1 + len(
            board.pieces(chess.KNIGHT, chess.BLACK)
        ) * 3 + len(
            board.pieces(chess.BISHOP, chess.BLACK)
        ) * 3 + len(
            board.pieces(chess.ROOK, chess.BLACK)
        ) * 5 + len(
            board.pieces(chess.QUEEN, chess.BLACK)
        ) * 9 + len(
            board.pieces(chess.KING, chess.BLACK)
        ) * 1
        
        # Max Possible material ((9*9) + (5*2) + (3*4))
        # / len(board.move_stack) to penalize point grabbing
        

        # King included so that material eval is never as strong as checkmate
        
        return (white_material - black_material) / (white_material + black_material) 


def check_first(board, move):
    # check checks, captures and promotions first
    # will be helpful for alpha beta pruning later
    return board.gives_check(move) or board.is_capture(move) or move.promotion == chess.QUEEN

def negamax_score(board, depth, color, states_eval=0):
    # legal_move_str = [str(move) for move in board.legal_moves]

    best_score = -9
    best_move = None
    
    for move in board.legal_moves:
        # print(move, depth, color)
        if check_first(board, move):
            # print("check_first")
            board.push(move)
            if board.is_checkmate():
                board.pop()
                states_eval += 1
                return move, color, states_eval
            
            elif depth < 0:
                score = score_board(board)
                states_eval += 1

            else:
                # print(f"{move} going deeper")
                response, score, states_eval = negamax_score(board, depth-1, -color, states_eval)
                
            board.pop()
            score *= color
            
            # print(f"{'.  ' * (2-depth)}, {color}, {move}, {score * color}")
            if score >= best_score:
                best_score = score
                best_move = move
        else:
            # print("check_last")
            board.push(move)
            if depth <= 1:
                score = score_board(board)
                states_eval += 1
            else:
                # print(f"{move} going deeper")
                response, score, states_eval = negamax_score(board, depth-1, -color, states_eval)
                
            board.pop()
            score *= color
            
            # print(f"{'.  ' * (2-depth)}, {color}, {move}, {score * color}")

            if score >= best_score:
                best_score = score
                best_move = move


    # for move in board.legal_moves:
    #     if not check_first(board, move):
    #         board.push(move)
    #         if board.is_checkmate():
    #             board.pop()
    #             return move, color
            
    #         elif depth == 0:
    #             score = score_board(board)

    #         else:
    #             response, score = negamax_score(board, depth-1, -color)

    #         board.pop()
    #         score *= color

    #         if score >= best_score:
    #             best_score = score
    #             best_move = move
    
    # print(f"{'.  ' * (2-depth)}, {color}, {best_move}, {best_score * color}")
    return best_move, best_score * color, states_eval

def negamax_alpha_beta(board, depth, color, alpha, beta, states_eval=0):
    best_score = -999
    best_move = None
    first_moves, last_moves = get_random_moves(board)
    # print(first_moves)
    legal_moves = first_moves + last_moves
    # print(f"c: {color}, d: {depth}")
    # print(legal_moves)
    for move in legal_moves:
        # print(f"looking into: {move}")
        board.push(move)
        if depth <= 0 or (move in first_moves and depth < 0):
            states_eval += 1
            score = score_board(board) # returns white's eval
            score *= color # correct eval for current color
            board.pop()
            return move, score, states_eval
        # print("going deeper")
        response, score, states_eval = negamax_alpha_beta(board=board, depth=depth-1, color=-color, alpha=-beta, beta=-alpha, states_eval=states_eval)
        score = -score
        # print(f"move: {move}, score: {score}")
        if score > best_score:
            best_score = score
            best_move = move
            if score > alpha:
                alpha = score

        if score >= beta:
            # move is good enough
            board.pop()
            return move, score, states_eval
        board.pop()
    
    if best_move is None:
        # no legal_moves
        # either checkmate or stalemate
        states_eval += 1
        score = score_board(board) # returns white's eval
        score *= color # correct eval for current color
        return None, score, states_eval
    
    return best_move, best_score, states_eval

def negamax_score_r(board, depth, color, states_eval=0):
    # legal_move_str = [str(move) for move in board.legal_moves]
    first_moves, last_moves = get_random_moves(board)
    legal_moves = first_moves + last_moves

    best_score = -9
    best_move = None
    
    for move in legal_moves:
        # print(move, depth, color)
        if check_first(board, move):
            # print("check_first")
            board.push(move)
            if board.is_checkmate():
                board.pop()
                states_eval += 1
                return move, color, states_eval
            
            elif depth < 0:
                score = score_board(board)
                states_eval += 1

            else:
                # print(f"{move} going deeper")
                response, score, states_eval = negamax_score(board, depth-1, -color, states_eval)
                
            board.pop()
            score *= color
            
            # print(f"{'.  ' * (2-depth)}, {color}, {move}, {score * color}")
            if score >= best_score:
                best_score = score
                best_move = move
        else:
            # print("check_last")
            board.push(move)
            if depth <= 1:
                score = score_board(board)
                states_eval += 1
            else:
                # print(f"{move} going deeper")
                response, score, states_eval = negamax_score(board, depth-1, -color, states_eval)
                
            board.pop()
            score *= color
            
            # print(f"{'.  ' * (2-depth)}, {color}, {move}, {score * color}")

            if score >= best_score:
                best_score = score
                best_move = move


    # for move in board.legal_moves:
    #     if not check_first(board, move):
    #         board.push(move)
    #         if board.is_checkmate():
    #             board.pop()
    #             return move, color
            
    #         elif depth == 0:
    #             score = score_board(board)

    #         else:
    #             response, score = negamax_score(board, depth-1, -color)

    #         board.pop()
    #         score *= color

    #         if score >= best_score:
    #             best_score = score
    #             best_move = move
    
    # print(f"{'.  ' * (2-depth)}, {color}, {best_move}, {best_score * color}")
    return best_move, best_score * color, states_eval

