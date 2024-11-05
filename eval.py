import chess
def get_color(board):
    return (len(board.move_stack) % 2) * 2 - 1

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
        ) * 9
        
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
        ) * 9
        
        # Max Possible material ((9*9) + (5*2) + (3*4))
        # / len(board.move_stack) to penalize point grabbing
        
        return (white_material - black_material) / (white_material + black_material) 
