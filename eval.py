import chess
def get_color(board):
    return ((len(board.move_stack) % 2) * 2 - 1) * (- 1)

def score_board(board):
    if board.can_claim_draw() or board.can_claim_fifty_moves() or board.can_claim_threefold_repetition():
        return 0
    if board.is_checkmate():
        return get_color(board)
    else:
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

def negamax_score(board, depth, color):
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
                return move, color
            
            elif depth == 0:
                score = score_board(board)

            else:
                # print(f"{move} going deeper")
                response, score = negamax_score(board, depth-1, -color)
                
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
            else:
                # print(f"{move} going deeper")
                response, score = negamax_score(board, depth-1, -color)
                
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
    return best_move, best_score * color