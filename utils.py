import chess
import numpy as np
import pandas as pd

def board_to_tensor(board):
    board_state = np.ndarray(shape=(0, 8, 8))
    for color in [chess.WHITE, chess.BLACK]:
        for piece in [
            chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING
        ]:

            mask = board.pieces_mask(piece, color)

            mask = np.array([float(i) for i in np.binary_repr(mask, width=64)]).reshape((1, 8, 8))
            board_state = np.concatenate((board_state, mask), axis=0)
    return board_state

def board_to_str(board):
    board_str = ""
    for color in [chess.WHITE, chess.BLACK]:
        for piece in [
            chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING
        ]:

            mask = board.pieces_mask(piece, color)

            board_str += np.binary_repr(mask, width=64)
    return board_str

def board_to_int_list(board):
    board_state = []
    for color in [chess.WHITE, chess.BLACK]:
        for piece in [
            chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN, chess.KING
        ]:

            mask = board.pieces_mask(piece, color)

            # mask = int(np.binary_repr(mask, width=64))
            board_state += [mask]
    return tuple(board_state)

def int_list_to_tensor(int_tuple):
    board_state = np.ndarray(shape=(0, 8, 8))
    for bit_board in int_tuple:

        mask = np.array([float(i) for i in np.binary_repr(bit_board, width=64)]).reshape((1, 8, 8))
        board_state = np.concatenate((board_state, mask), axis=0)
    return board_state

def tensor_to_int_list(tensor):
    board_state = []
    for i in range(12):
        mask = tensor[i, :, :].flatten()
        # bit_board = mask.dot(2**np.arange(mask.size)[::-1])
        bit_board = mask.dot(1 << np.arange(mask.size)[::-1])
        board_state += [int(bit_board)]
    return tuple(board_state)

def flip_tensor(tensor):
    return np.concatenate((tensor[6:12, ::-1], tensor[0:6, ::-1]), axis=0)

def tensor_to_str_board(tensor):
    str_board = np.array(["."]*64).reshape((8, 8))
    str_board[tensor[0]==1] = "P"
    str_board[tensor[1]==1] = "R"
    str_board[tensor[2]==1] = "N"
    str_board[tensor[3]==1] = "B"
    str_board[tensor[4]==1] = "Q"
    str_board[tensor[5]==1] = "K"
    str_board[tensor[6]==1] = "p"
    str_board[tensor[7]==1] = "r"
    str_board[tensor[8]==1] = "n"
    str_board[tensor[9]==1] = "b"
    str_board[tensor[10]==1] = "q"
    str_board[tensor[11]==1] = "k"
    str_board = str_board[:, ::-1]
    return str(str_board)

def add_df_to_db(path, df):
    db = pd.read_csv(path)
    db = pd.concat((df, db), axis=0)
    db.to_csv(path, index=False)
    print(db)