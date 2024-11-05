import chess
from eval import score_board
from utils import board_to_int_list
from matplotlib import pyplot as plt
import time
import pandas as pd

def print_board(board):
    str_arr = ["  a b c d e f g h  "]
    for i, s in enumerate(str(board).split("\n")):
        str_arr += [f"{8-i} {s} {8-i}"]
    str_arr += ["  a b c d e f g h  "]
    print("\n".join(str_arr))

class Gym:
    def __init__(self, board, turn_limit=50) -> None:
        self.board = board
        self.turn_limit = turn_limit

    def human_human_game(self, save=False):
        self.board.reset()
        
        board = self.board
        state_df = None
        htc = 0

        while not board.is_game_over():
            # Player Move
            print_board(board)
            legal_moves = [str(move) for move in self.board.legal_moves]
            p_move = ""
            while p_move not in legal_moves:
                time.sleep(1)
                print("Player Move: ", end="")
                p_move = input()
                print(p_move)

                if p_move == "quit":
                    return score_board(board), state_df
                if p_move not in legal_moves:
                    print(legal_moves)
            if save:
                bit_board = board_to_int_list(board)
                state_df = pd.concat((state_df, pd.DataFrame([[bit_board, htc % 2, p_move, "human"]], columns=["state", "color", "move", "player"])), axis=0)
            board.push_san(p_move)
            htc += 1

            if board.is_game_over():
                return score_board(board), state_df

        return score_board(board), state_df

    def human_bot_game(self, agent, human_white=True, save=False):
        self.board.reset()
        agent.reset()
        agent.board = self.board
        board = self.board
        state_df = None
        htc = 0

        if not human_white:
            bot_move = agent.move()
            print(f"Bot Move: {bot_move}")

            if save:
                bit_board = board_to_int_list(board)
                state_df = pd.concat((state_df, pd.DataFrame([[bit_board, htc % 2, bot_move, "bot"]], columns=["state", "color", "move", "player"])), axis=0)
            
            board.push_san(bot_move)
            htc += 1
            if board.is_game_over():
                return score_board(board), state_df

        while not board.is_game_over():
            # Player Move
            print_board(board)
            legal_moves = [str(move) for move in self.board.legal_moves]
            p_move = ""
            while p_move not in legal_moves:
                time.sleep(1)
                print("Player Move: ", end="")
                p_move = input()
                print(p_move)

                if p_move == "quit":
                    return score_board(board), state_df
                if p_move not in legal_moves:
                    print(legal_moves)
            if save:
                bit_board = board_to_int_list(board)
                state_df = pd.concat((state_df, pd.DataFrame([[bit_board, htc % 2, p_move, "human"]], columns=["state", "color", "move", "player"])), axis=0)
            board.push_san(p_move)
            htc += 1

            bot_move = agent.move()
            print(f"Bot Move: {bot_move}")

            if save:
                bit_board = board_to_int_list(board)
                state_df = pd.concat((state_df, pd.DataFrame([[bit_board, htc % 2, bot_move, "bot"]], columns=["state", "color", "move", "player"])), axis=0)
            
            board.push_san(bot_move)
            htc += 1
            if board.is_game_over():
                return score_board(board), state_df

        return score_board(board), state_df
        

    def game(self, agent_w, agent_b, show=False, save=False):
        self.board.reset()
        agent_w.reset()
        agent_b.reset()
        state_df = None

        board = self.board
            
        for i in range(self.turn_limit):
            board.push_san(agent_w.move())
            if save:
                bit_board = board_to_int_list(board)
                state_df = pd.concat((state_df, pd.DataFrame([[bit_board, 0]], columns=["state", "color"])), axis=0)
            if board.is_game_over():
                result = score_board(board)
                if save:
                    state_df["result"] = result
                return result, state_df
            
            board.push_san(agent_b.move())
            if save:
                bit_board = board_to_int_list(board)
                state_df = pd.concat((state_df, pd.DataFrame([[bit_board, 1]], columns=["state", "color"])), axis=0)
            if board.is_game_over():
                result = score_board(board)
                if save:
                    state_df["result"] = result
                return result, state_df
            if show:
                print(board)
                print("-"*16)
        # hit turn limit
        result = score_board(board)
        if save:
            state_df["result"] = result
        return result, state_df
    
    def tournament(self, agent_1, agent_2, num_games_white=50, show=False, save=False):
        score = 0
        agent_1_wins = 0
        agent_2_wins = 0
        all_state_df = None

        for i in range(num_games_white):
            self.board.reset()
            agent_1.reset()
            agent_2.reset()
            result, state_df = self.game(agent_1, agent_2, show, save=save)
            if save:
                state_df["result"] = result
                all_state_df = pd.concat((all_state_df, state_df), axis=0)
            score += result
            if result == 1:
                agent_1_wins += 1
            if result == -1:
                agent_2_wins += 1
            
        for i in range(num_games_white):
            self.board.reset()
            agent_1.reset()
            agent_2.reset()
            result, state_df = self.game(agent_2, agent_1, show, save=save)
            if save:
                state_df["result"] = result
                all_state_df = pd.concat((all_state_df, state_df), axis=0)
            score -= result
            if result == 1:
                agent_2_wins += 1
            if result == -1:
                agent_1_wins += 1

        return score, (agent_1_wins, agent_2_wins)

        

