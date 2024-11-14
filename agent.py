import numpy as np
from opening_tree import DataBaseOpeningSystem
from eval import score_board, get_color, negamax_score_r, negamax_alpha_beta
from utils import board_to_int_list

class Agent:
    def __init__(self, board) -> None:
        self.board = board
    
    def move(self):
        raise NotImplementedError
    
    def reset(self):
        pass

class RandomAgent(Agent):
    def move(self):
        legal_moves = [str(move) for move in self.board.legal_moves]
        return np.random.choice(legal_moves)

class VaudOpenAgent(Agent):
    def __init__(self, board, depth=2, db_paths=[
            "opening_db\\vaud_vs_rand.csv", 
            "opening_db\\gotham_london.csv",
            "opening_db\\gotham_catalan.csv"
            ]) -> None:
        super().__init__(board)
        self.opening_bot = DataBaseOpeningSystem(db_paths)
        self.state = "$EARLY$"
        self.color = None
        self.depth = depth
    
    def move(self):
        legal_moves = [str(move) for move in self.board.legal_moves]
        if self.state == "$EARLY$":
            move = self.opening_bot.move(board_to_int_list(self.board))

            if move not in legal_moves:
                self.state = "$MID$"
                return self.move()
            else:
                return move
        elif self.state == "$MID$":

            color = -get_color(self.board)
            # print(color)
            # best_move, score, _ = negamax_score_r(self.board, self.depth, color)
            best_move, score, _ = negamax_alpha_beta(self.board, self.depth, color, -99, 99, 0)
            # print(best_move, score)
            return str(best_move)

    def reset(self):
        self.__init__(self.board)

