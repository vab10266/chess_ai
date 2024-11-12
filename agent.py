import numpy as np
from opening_tree import DataBaseOpeningSystem
from eval import score_board, get_color, negamax_score
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
    def __init__(self, board, depth=2) -> None:
        super().__init__(board)
        self.opening_bot = DataBaseOpeningSystem([
            "opening_db\\vaud_vs_rand.csv", 
            "opening_db\\gotham_london.csv",
            "opening_db\\gotham_catalan.csv"
            ])
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
            # eval_dict = {}
            # best_move = legal_moves[0]
            # best_score = -999
            color = get_color(self.board)
            # print(color)
            # for move in legal_moves:
            #     self.board.push_san(move)
            #     score = score_board(self.board)
            #     score *= color
            #     if score >= best_score:
            #         best_score = score
            #         best_move = move
            #     eval_dict[move] = score
            #     self.board.pop()
            # if color == -1:
            print("*-"*10)
            best_move, score = negamax_score(self.board, self.depth, color)
            # elif color == 1:
            #     move, score = maximize_score(self.board, self.depth)
                
            return str(best_move)

    def reset(self):
        self.__init__(self.board)

