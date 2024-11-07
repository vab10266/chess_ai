
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
        # print(len(self.board.move_stack))
        if len(self.board.move_stack) % 2 == 1:
            str_arr = str_arr[::-1]
            for i in range(8):
                str_arr[i] = str_arr[i][::-1]
        # print(str_arr)

        for row in range(8):
            for col in range(8):
                piece = str_arr[row][col]
                if piece != ".":
                    if piece == "P" or piece == "p":
                        shifts = (20, 30)
                    else: 
                        shifts = (10, 10)
                    self.screen.blit(
                        self.image_dict[piece], (col * 100 + shifts[0], row * 100 + shifts[1])
                    )

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
        # main game loop
        run = True
        while run:
            self.timer.tick(self.fps)
            if self.frame_count < self.flash_cycle_length:
                self.frame_count += 1
            else:
                self.frame_count = 0
                
            self.draw_board()
            self.draw_pieces()

            pygame.display.update()
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:

                    x_coord = event.pos[0] // 100
                    y_coord = event.pos[1] // 100
                    click_coords = (x_coord, y_coord)
                    print(click_coords)
                    if self.state.value < 2:
                        partial_move = f"{chr(97+x_coord)}{8-y_coord}"
                    else:
                        partial_move = f"{chr(104-x_coord)}{1+y_coord}"

                    print(partial_move)
                    if self.state == GuiState.white_to_move:
                        self.state = GuiState.white_selected
                        move += partial_move
                    elif self.state == GuiState.white_selected:
                        self.state = GuiState.black_to_move
                        move += partial_move
                        print(move)
                        self.board.push_san(move)
                        move = ""
                    elif self.state == GuiState.black_to_move:
                        self.state = GuiState.black_selected
                        move += partial_move
                    elif self.state == GuiState.black_selected:
                        self.state = GuiState.white_to_move
                        move += partial_move
                        print(move)
                        self.board.push_san(move)
                        move = ""
                    
if __name__ == "__main__":
    g = GUI()
    g.open()
