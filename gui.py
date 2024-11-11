
# Importing Modules
import pandas as pd
import pygame
import chess
from enum import Enum
from agent import Agent, RandomAgent, VaudOpenAgent
from utils import board_to_int_list, add_df_to_db, square_coords_to_screen_coords, screen_coords_to_square_coords, square_coords_to_name, square_num_to_square_coords

class GuiState(Enum):
    white_to_move = 0
    white_selected = 1
    black_to_move = 2
    black_selected = 3

class GUI:
    def __init__(
            self,
            width: int = 800,
            height: int = 800,
            fps: int = 60,
            dark_color: list = [187,190,100],
            light_color: list = [234,240,206],
            save_white=True,
            save_black=False,
            white_player = "human",
            black_player = "human",
            save_path="opening_db\\vaud_vs_rand.csv"
        ) -> None:
                
        self.state = GuiState.white_to_move
        self.width = width
        self.height = height
        self.fps = fps
        self.dark_color = dark_color
        self.light_color = light_color

        self.frame_count = 0
        self.flash_cycle_length = 30

        self.board = chess.Board()
        self.save_white = save_white
        self.save_black = save_black
        self.state_df = None
        self.path = save_path

        if type(white_player) != str and issubclass(white_player, Agent):
            self.white_player = white_player(self.board)
        else:
            self.white_player = None

        if type(black_player) != str and issubclass(black_player, Agent):
            self.black_player = black_player(self.board)
        else:
            self.black_player = None
        
    # draw main game board
    def draw_board(self):
        self.screen.fill(self.dark_color)
        for i in range(32):

            column = i % 4
            row = i // 4

            if row % 2 == 0:
                pygame.draw.rect(
                    self.screen, 
                    self.light_color, 
                    [
                        600 - (column * 200), 
                        row * 100, 
                        100, 
                        100
                    ]
                )
            else:
                pygame.draw.rect(
                    self.screen, 
                    self.light_color, 
                    [
                        700 - (column * 200), 
                        row * 100, 
                        100, 
                        100
                    ]
                )
        pygame.draw.rect(self.screen, 'gray', [0, 800, self.width, 100])
        pygame.draw.rect(self.screen, 'gold', [0, 800, self.width, 100], 5)
        pygame.draw.rect(self.screen, 'gold', [800, 0, 200, self.height], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                    'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        self.screen.blit(self.big_font.render(
            status_text[self.state.value], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(self.screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(self.screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        self.screen.blit(self.medium_font.render('FORFEIT', True, 'black'), (810, 830))

    def draw_pieces(self):
        str_arr = str(self.board).replace(" ", "").split("\n")

        if len(self.board.move_stack) % 2 == 1:
            str_arr = str_arr[::-1]
            for i in range(8):
                str_arr[i] = str_arr[i][::-1]

        for row in range(8):
            for col in range(8):
                piece = str_arr[row][col]
                if piece != ".":
                    if piece == "P" or piece == "p":
                        shifts = (15, 30)
                    else: 
                        shifts = (10, 10)
                    self.screen.blit(
                        self.image_dict[piece], (col * 100 + shifts[0], row * 100 + shifts[1])
                    )

    def draw_valid_moves(self, square_clicked):
        if self.state.value < 2:
            color = 'red'
        else:
            color = 'blue'
        
        for move in self.board.legal_moves:
            if move.from_square == square_clicked:
                r, f = square_num_to_square_coords(move.to_square)
                x, y = square_coords_to_screen_coords(r, f,self.state.value < 2)
                
                pygame.draw.circle(
                    self.screen, 
                    color, 
                    (
                        x * 100 + 50, 
                        y * 100 + 50
                    ), 5)
                
        pygame.display.update()

    def white_move(self, move):
        if move in [str(m) for m in self.board.legal_moves]:
            print(f"White: {move}")
            self.state = GuiState.black_to_move
            if self.save_white:
                bit_board = board_to_int_list(self.board)
                self.state_df = pd.concat((
                    self.state_df, 
                    pd.DataFrame(
                        [[
                            bit_board, 
                            len(self.board.move_stack) % 2,
                            move, 
                            "human" if self.white_player is None else 'bot'
                        ]], columns=["state", "color", "move", "player"]
                    )
                ), axis=0)
            self.board.push_san(move)

        elif f"{move}q" in [str(m) for m in self.board.legal_moves]:
            move = f"{move}q"
            print(f"White: {move}")
            self.state = GuiState.black_to_move
            if self.save_white:
                bit_board = board_to_int_list(self.board)
                self.state_df = pd.concat((
                    self.state_df, 
                    pd.DataFrame(
                        [[
                            bit_board, 
                            len(self.board.move_stack) % 2,
                            move, 
                            "human" if self.white_player is None else 'bot'
                        ]], columns=["state", "color", "move", "player"]
                    )
                ), axis=0)
            self.board.push_san(move)

        else:
            self.state = GuiState.white_to_move
        self.draw_board()
        self.draw_pieces()
    
    def black_move(self, move):
        if move in [str(m) for m in self.board.legal_moves]:
            print(f"Black: {move}")
            self.state = GuiState.white_to_move
            if self.save_black:
                bit_board = board_to_int_list(self.board)
                self.state_df = pd.concat((
                    self.state_df, 
                    pd.DataFrame(
                        [[
                            bit_board, 
                            len(self.board.move_stack) % 2,
                            move, 
                            "human" if self.black_player is None else 'bot'
                        ]], columns=["state", "color", "move", "player"]
                    )
                ), axis=0)
            self.board.push_san(move)

        elif f"{move}q" in [str(m) for m in self.board.legal_moves]:
            move = f"{move}q"
            print(f"Black: {move}")
            self.state = GuiState.white_to_move
            if self.save_black:
                bit_board = board_to_int_list(self.board)
                self.state_df = pd.concat((
                    self.state_df, 
                    pd.DataFrame(
                        [[
                            bit_board, 
                            len(self.board.move_stack) % 2,
                            move, 
                            "human" if self.black_player is None else 'bot'
                        ]], columns=["state", "color", "move", "player"]
                    )
                ), axis=0)
            self.board.push_san(move)
                
        else:
            self.state = GuiState.black_to_move
        self.draw_board()
        self.draw_pieces()

    def restart(self):
        self.game_over = False
        self.move = ""
        if self.save_white or self.save_black:                        
             (self.path, self.state_df)
        self.board.reset()

        self.draw_board()
        self.draw_pieces()
        self.state = GuiState.white_to_move

        pygame.display.update()
                
    def open(self):
        pygame.init()

        self.screen = pygame.display.set_mode([self.width, self.height])
        
        pygame.display.set_caption('Two-Player Chess Game')

        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)

        self.timer = pygame.time.Clock()

        
        self.image_dict = load_pieces()
        winner = ''
        self.game_over = False
        self.move = ""

        self.draw_board()
        self.draw_pieces()
        pygame.display.update()

        # main game loop
        run = True
        while run:
            self.timer.tick(self.fps)
            if self.frame_count < self.flash_cycle_length:
                self.frame_count += 1
            else:
                self.frame_count = 0
            
            if not self.game_over:
                    
                if self.white_player is not None and self.state == GuiState.white_to_move:
                    self.move = self.white_player.move()
                    self.white_move(self.move)
                
                if self.black_player is not None and self.state == GuiState.black_to_move:
                    self.move = self.black_player.move()
                    self.black_move(self.move)
                
                # event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                        x_coord = event.pos[0] // 100
                        y_coord = event.pos[1] // 100
                        click_coords = (x_coord, y_coord)

                        rank_clicked, file_clicked = screen_coords_to_square_coords(x_coord, y_coord, self.state.value < 2)
                        partial_move = square_coords_to_name(rank_clicked, file_clicked)
                        
                        square_clicked = chess.square(file_clicked, rank_clicked)
                        color_clicked = self.board.color_at(square_clicked)

                        if self.state == GuiState.white_to_move:
                            # [print(m, end=", ") for m in self.board.legal_moves]
                            # print()
                            self.move = ""
                            if color_clicked == True:
                                self.state = GuiState.white_selected
                                self.move += partial_move
                                self.draw_valid_moves(square_clicked)
                            else:
                                self.move = ""

                        elif self.state == GuiState.white_selected:
                            self.move += partial_move
                            self.white_move(self.move)

                        elif self.state == GuiState.black_to_move:
                            self.move = ""
                            if color_clicked == False:
                                self.state = GuiState.black_selected
                                self.move += partial_move
                                self.draw_valid_moves(square_clicked)
                            else:
                                self.move = ""

                        elif self.state == GuiState.black_selected:
                            self.move += partial_move
                            self.black_move(self.move)
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        # print("restart")
                        self.restart()
                    pygame.display.update()
                    
                if self.board.is_game_over():
                    self.draw_board()
                    self.draw_pieces()

                    pygame.display.update()
                    pygame.draw.rect(self.screen, 'black', [200, 360, 400, 80])
                    self.screen.blit(self.font.render(
                        f'Result: {self.board.result()}!', True, 'white'), (210, 390))
                    
                    pygame.display.update()
                    self.game_over = True
                    
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.restart()

        if self.save_white or self.save_black:                        
            add_df_to_db(self.path, self.state_df)

def load_pieces():
    # load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
    black_queen = pygame.image.load('./images/black_queen.png')
    black_queen = pygame.transform.scale(black_queen, (80, 80))
    black_queen_small = pygame.transform.scale(black_queen, (45, 45))
    black_king = pygame.image.load('./images/black_king.png')
    black_king = pygame.transform.scale(black_king, (80, 80))
    black_king_small = pygame.transform.scale(black_king, (45, 45))
    black_rook = pygame.image.load('./images/black_rook.png')
    black_rook = pygame.transform.scale(black_rook, (80, 80))
    black_rook_small = pygame.transform.scale(black_rook, (45, 45))
    black_bishop = pygame.image.load('./images/black_bishop.png')
    black_bishop = pygame.transform.scale(black_bishop, (80, 80))
    black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
    black_knight = pygame.image.load('./images/black_knight.png')
    black_knight = pygame.transform.scale(black_knight, (80, 80))
    black_knight_small = pygame.transform.scale(black_knight, (45, 45))
    black_pawn = pygame.image.load('./images/black_pawn.png')
    black_pawn = pygame.transform.scale(black_pawn, (65, 65))
    black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
    white_queen = pygame.image.load('./images/white_queen.png')
    white_queen = pygame.transform.scale(white_queen, (80, 80))
    white_queen_small = pygame.transform.scale(white_queen, (45, 45))
    white_king = pygame.image.load('./images/white_king.png')
    white_king = pygame.transform.scale(white_king, (80, 80))
    white_king_small = pygame.transform.scale(white_king, (45, 45))
    white_rook = pygame.image.load('./images/white_rook.png')
    white_rook = pygame.transform.scale(white_rook, (80, 80))
    white_rook_small = pygame.transform.scale(white_rook, (45, 45))
    white_bishop = pygame.image.load('./images/white_bishop.png')
    white_bishop = pygame.transform.scale(white_bishop, (80, 80))
    white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
    white_knight = pygame.image.load('./images/white_knight.png')
    white_knight = pygame.transform.scale(white_knight, (80, 80))
    white_knight_small = pygame.transform.scale(white_knight, (45, 45))
    white_pawn = pygame.image.load('./images/white_pawn.png')
    white_pawn = pygame.transform.scale(white_pawn, (65, 65))
    white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

    return {
        "P": white_pawn,
        "R": white_rook,
        "N": white_knight,
        "B": white_bishop,
        "Q": white_queen,
        "K": white_king,
        "p": black_pawn,
        "r": black_rook,
        "n": black_knight,
        "b": black_bishop,
        "q": black_queen,
        "k": black_king,
    }

if __name__ == "__main__":
    g = GUI(
        white_player="human",
        black_player=RandomAgent,
        save_path="opening_db\\vaud_vs_rand.csv",
        save_white=False,
        save_black=False,
    )
    g.open()
