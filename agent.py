import numpy as np
from opening_tree import VaudOpeningSystem
from eval import score_board, get_color

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
    def __init__(self, board) -> None:
        super().__init__(board)
        self.opening_bot = VaudOpeningSystem()
        self.state = "$EARLY$"
        self.color = None
    
    def move(self):
        legal_moves = [str(move) for move in self.board.legal_moves]
        if self.state == "$EARLY$":
            try:
                move = self.opening_bot.move(self.board.peek())
            except IndexError:
                move = self.opening_bot.move("init")

            if move not in legal_moves:
                self.state = "$MID$"
                return self.move()
            else:
                return move
        elif self.state == "$MID$":
            eval_dict = {}
            best_move = legal_moves[0]
            best_score = -999
            color = get_color(self.board) * -1
            # print(color)
            for move in legal_moves:
                self.board.push_san(move)
                score = score_board(self.board)
                score *= color
                if score >= best_score:
                    best_score = score
                    best_move = move
                eval_dict[move] = score
                self.board.pop()
            # print(eval_dict)
            # print(best_move, best_score * color)
            return best_move

    def reset(self):
        self.opening_bot = VaudOpeningSystem()
        self.state = "$EARLY$"
        self.color = None