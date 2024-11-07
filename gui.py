
# Importing Modules
import pygame
import chess
from enum import Enum

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
        # self.board.push_san("d2d4")
        # self.board.push_san("d7d5")
 
    def square_coords_to_screen_coords(self, rank, file):
        if self.state.value < 2:
            y_coord = 7 - rank
            x_coord = file
        else:
            y_coord = rank
            x_coord = 7 - file
        return x_coord, y_coord

    def screen_coords_to_square_coords(self, x_coord, y_coord):
        if self.state.value < 2:
            rank = 7 - y_coord
            file = x_coord
        else:
            rank = y_coord
            file = 7 - x_coord
        return rank, file
    
    def square_coords_to_name(self, rank, file):
        return f"{chr(97+file)}{rank+1}"
    
    def square_num_to_square_coords(self, sq_num):
        return sq_num // 8, sq_num % 8
    
    # draw main game board
    def draw_board(self):
        self.screen.fill(self.dark_color)
        # print("drawing board")
        for i in range(32):

            column = i % 4
            row = i // 4
            # print(row, column)

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
                r, f = self.square_num_to_square_coords(move.to_square)
                x, y = self.square_coords_to_screen_coords(r, f)
                
                pygame.draw.circle(
                    self.screen, 
                    color, 
                    (
                        x * 100 + 50, 
                        y * 100 + 50
                    ), 5)
                
        pygame.display.update()


    def open(self):
        pygame.init()

        self.screen = pygame.display.set_mode([self.width, self.height])
        
        pygame.display.set_caption('Two-Player Chess Game')

        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)

        self.timer = pygame.time.Clock()

                
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

        self.image_dict = {
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
        
        winner = ''
        game_over = False
        move = ""

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
            
            if not game_over:
                    

                # event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:

                        x_coord = event.pos[0] // 100
                        y_coord = event.pos[1] // 100
                        click_coords = (x_coord, y_coord)

                        rank_clicked, file_clicked = self.screen_coords_to_square_coords(x_coord, y_coord)
                        partial_move = self.square_coords_to_name(rank_clicked, file_clicked)
                        # print(rank_clicked, file_clicked)
                        # print(partial_move)
                        
                        square_clicked = chess.square(file_clicked, rank_clicked)
                        color_clicked = self.board.color_at(square_clicked)
                        print(color_clicked)

                        if self.state == GuiState.white_to_move:
                            if color_clicked == True:
                                self.state = GuiState.white_selected
                                move += partial_move
                                self.draw_valid_moves(square_clicked)
                            else:
                                move = ""
                            print(move)

                        elif self.state == GuiState.white_selected:
                            move += partial_move
                            if move in [str(m) for m in self.board.legal_moves]:
                                self.state = GuiState.black_to_move
                                self.board.push_san(move)

                            else:
                                self.state = GuiState.white_to_move

                            self.draw_board()
                            self.draw_pieces()
                            move = ""

                        elif self.state == GuiState.black_to_move:
                            if color_clicked == False:
                                self.state = GuiState.black_selected
                                move += partial_move
                                self.draw_valid_moves(square_clicked)
                            else:
                                move = ""

                        elif self.state == GuiState.black_selected:
                            move += partial_move
                            if move in [str(m) for m in self.board.legal_moves]:
                                self.state = GuiState.white_to_move
                                self.board.push_san(move)

                            else:
                                self.state = GuiState.black_to_move

                            self.draw_board()
                            self.draw_pieces()
                            move = ""
                    
                    pygame.display.update()
                    
                if self.board.is_game_over():
                    self.draw_board()
                    self.draw_pieces()

                    pygame.display.update()
                    pygame.draw.rect(self.screen, 'black', [200, 360, 400, 80])
                    self.screen.blit(self.font.render(
                        f'Result: {self.board.result()}!', True, 'white'), (210, 390))
                    
                    pygame.display.update()
                    game_over = True
                    
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        game_over = False
                        move = ""
                        self.board.reset()

                        self.draw_board()
                        self.draw_pieces()

                        pygame.display.update()


if __name__ == "__main__":
    g = GUI()
    g.open()
    # for rank in range(8):
    #     for file in range(8):
    #         x, y = g.square_coords_to_screen_coords(rank, file)
    #         print(g.square_coords_to_name(rank, file), rank, file)
    #         print(x, y)
    #         r, f = g.screen_coords_to_square_coords(x, y)
    #         print(g.square_coords_to_name(r, f), r, f)
