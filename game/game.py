from collections import defaultdict
import pygame
from game.board import Board
from utils.gameobject import GameObject
import globals
from game.piece import PieceType, PieceColor
from utils.image import load_image
from game.piece import Piece
from game.engine import Engine
from utils.zobrist import Zobrist

class Game(GameObject):
    _instance = None

    def __new__(cls, screen, square_size):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, screen, square_size):
        if not hasattr(self, 'initialized'):
            self.screen = screen
            self.square_size = square_size
            self.board = Board(columns=8, rows=8, light_cell_color=(232,237,249), dark_cell_color=(183,192,216), square_size=square_size, screen=screen)
            self.selected_piece = None
            self.selected_coord = None
            self.dragging = False
            self.legal_moves = None
            self.initialized = True
            self.current_turn: PieceColor = PieceColor.WHITE
            self.player_turn: PieceColor = PieceColor.WHITE
            self.ai_turn: PieceColor = PieceColor.BLACK
            if self.player_turn == PieceColor.BLACK:
                self.ai_turn = PieceColor.WHITE
            self.engine = Engine(self.board, self.ai_turn)
            self.game_end = False
            self.zobrist = Zobrist(self.board)
            self.history = []
            self.repetition_count = defaultdict(int)
            globals.game_instance = self
    
    def update(self):
        if self.is_draw_by_repetition():
            self.display_draw("Draw by Repetition")
            self.game_end = True
            return

        if self.is_draw_by_stalemate():
            self.display_draw("Draw by Stalemate")
            self.game_end = True
            return
        return self.board.update()

    def display_draw(self, draw_reason):
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(draw_reason, True, (255, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        exit()
    
    def is_draw_by_repetition(self):
        board_hash = self.zobrist.compute_hash()
        return self.repetition_count[board_hash] >= 3

    def is_draw_by_stalemate(self):
        return not self.is_checkmate(self.current_turn) and not self.has_valid_moves(self.current_turn)

    def is_checkmate(self, color: PieceColor):
        opponent_color = PieceColor.WHITE if color == PieceColor.BLACK else PieceColor.BLACK
        opponent_king_pos = self.get_king_position(opponent_color)

        if self.is_king_in_check(opponent_king_pos, opponent_color):
            if not self.has_valid_moves(opponent_color):
                return True
        return False

    def is_king_in_check(self, king_pos, color: PieceColor):
        opponent_color = PieceColor.WHITE if color == PieceColor.BLACK else PieceColor.BLACK
        threat_coords = self.board.generate_threat_map(opponent_color, self.board.representation)
        return king_pos in threat_coords

    def get_king_position(self, color: PieceColor):
        for coord, piece in self.board.representation.items():
            if piece.name == PieceType.KING and piece.color == color:
                return coord
        return None
    
    def has_valid_moves(self, color: PieceColor):
        for coord, piece in self.board.representation.items():
            if piece.color == color:
                legal_moves = piece.get_legal_moves(coord, self.board.representation)
                for move in legal_moves:
                    if not self.king_will_be_in_danger(self.board.representation, coord, piece, move, color):
                        return True
        return False

    def display_victory(self, color: PieceColor):
        winner = "White" if color == PieceColor.BLACK else "Black"
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"{winner} wins by Checkmate!", True, (255, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        exit()

    def run(self):
        run = True
        ai_waiting = False  
        ai_wait_frames = 10  
        ai_wait_counter = 0

        while run:
            self.update()

            if self.dragging:
                self.handle_piece_drag()

            if not self.game_end and self.current_turn == self.ai_turn and not self.dragging:
                if ai_waiting:  
                    ai_wait_counter += 1
                    if ai_wait_counter >= ai_wait_frames:
                        self.engine.make_move()  
                        self.change_turn()
                        ai_waiting = False  
                        ai_wait_counter = 0  
                else:
                    ai_waiting = True  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(event.pos)
            pygame.display.update()

        pygame.quit()


    def handle_mouse_down(self, pos):
        col, row = pos[0] // self.square_size, pos[1] // self.square_size
        self.selected_coord = (col, row)
        self.selected_piece = self.board.get_piece_obj_on_pos(self.selected_coord)
        if self.selected_piece and self.selected_piece.color == self.current_turn and self.current_turn == self.player_turn:
            legal_moves_cadiates = self.selected_piece.get_legal_moves(self.selected_coord, self.board.representation)
            self.legal_moves = []
            castling_legal = []
            for legal_move in legal_moves_cadiates:
                if not self.king_will_be_in_danger(self.board.representation, self.selected_coord, self.selected_piece, legal_move, self.current_turn):
                    self.legal_moves.append(legal_move)
            if self.selected_piece == PieceType.KING:
                for lm in self.legal_moves:
                    current_col, _ = self.selected_coord
                    lm_col, _ = lm
                    offset = lm_col - current_col
                    if offset > 1 or offset < -1:
                        castling_legal.append(lm)
                self.legal_moves = castling_legal
            # del[self.board.representation[self.selected_coord]]
            self.selected_piece.showing = False
            self.dragging = True

    def handle_mouse_up(self, pos):
        if self.dragging:
            col, row = pos[0] // self.square_size, pos[1] // self.square_size
            col_selected, row_selected = self.selected_coord
            if self.legal_moves is not None:
                if (col, row) in self.legal_moves:
                    if self.selected_piece.name == PieceType.KING:
                        offset = col - col_selected
                        if offset == 2:
                            self.board.representation[(col - 1, row)] = self.board.representation[(col + 1, row)]
                            del[self.board.representation[(col + 1, row)]]
                        elif offset == -2:
                            self.board.representation[(col + 1, row)] = self.board.representation[(col - 2, row)]
                            del[self.board.representation[(col - 2, row)]]
                    if self.selected_piece.name == PieceType.PAWN:
                        piece_at_target = self.board.representation.get((col, row), None)
                        if piece_at_target is None:
                            offset = (col_selected - col, row_selected - row)
                            increment = 1 if self.selected_piece.color == PieceColor.WHITE else -1
                            offsets = [-1, 1]
                            for os in offsets:
                                if offset == (os, increment):
                                    del[self.board.representation[(col_selected - os, row_selected)]]  
                    
                    self.board.representation[(col, row)] = self.selected_piece
                    del[self.board.representation[self.selected_coord]]
                    self.selected_piece.showing = True
                    if (self.selected_piece.name == PieceType.PAWN and self.selected_piece.color == PieceColor.WHITE and row == 0) or \
                       (self.selected_piece.name == PieceType.PAWN and self.selected_piece.color == PieceColor.BLACK and row == 7):
                        self.show_promotion_ui((col, row))
                    if self.is_checkmate(self.current_turn):
                        self.game_end = True
                        victory = PieceColor.WHITE if self.current_turn == PieceColor.BLACK else PieceColor.BLACK
                        self.display_victory(victory)
                    
                    if self.selected_piece:
                        self.selected_piece.increment_num_of_moves()  
                    self.change_turn()
                    
                else:
                    self.board.representation[self.selected_coord] = self.selected_piece
                    self.selected_piece.showing = True
            self.dragging = False
            self.selected_piece = None
            self.legal_moves = None
    
    def change_turn(self):
        if self.current_turn == PieceColor.WHITE:
            self.current_turn = PieceColor.BLACK
        else:
            self.current_turn = PieceColor.WHITE
        current_hash = self.zobrist.compute_hash()
        self.history.append(current_hash)
        self.repetition_count[current_hash] += 1

    def king_will_be_in_danger(self, representation, selected_coord, selected_piece, target_coord, turn):
        clone_representation = representation.copy()
        col, row = target_coord

        if selected_coord in clone_representation:
            del clone_representation[selected_coord]
        clone_representation[(col, row)] = selected_piece

        king_position = None
        for coord, piece in clone_representation.items():
            if piece.name == PieceType.KING and piece.color == turn:
                king_position = coord
                break

        if not king_position:
            raise ValueError("King not found on the board")

        opponent = PieceColor.WHITE if turn == PieceColor.BLACK else PieceColor.BLACK
        threat_coords = self.board.generate_threat_map(opponent, clone_representation)

        if king_position in threat_coords:
            return True
        return False

    def handle_piece_drag(self):
         if self.selected_piece is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            piece_image = self.selected_piece.image
            piece_rect = piece_image.get_rect()
            piece_rect.topleft = (mouse_x - piece_rect.width // 2, mouse_y - piece_rect.height // 2)
            self.screen.blit(piece_image, piece_rect.topleft)
    
    def show_promotion_ui(self, target_coord):
        piece_options = [
            (PieceType.QUEEN, load_image(f"assets/{self.selected_piece.color.value}_queen.png", 80, 80)),
            (PieceType.ROOK, load_image(f"assets/{self.selected_piece.color.value}_rook.png", 80, 80)),
            (PieceType.BISHOP, load_image(f"assets/{self.selected_piece.color.value}_bishop.png", 80, 80)),
            (PieceType.KNIGHT, load_image(f"assets/{self.selected_piece.color.value}_knight.png", 80, 80)),
        ]

        box_width, box_height = 320, 80
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = (self.screen.get_height() - box_height) // 2
        pygame.draw.rect(self.screen, (200, 200, 200), (box_x, box_y, box_width, box_height))
        num_options = len(piece_options)
        button_width = box_width // num_options

        for i, (piece_type, image) in enumerate(piece_options):
            button_x = box_x + i * button_width + (button_width - 80) // 2
            button_y = box_y + (box_height - 80) // 2
            image_rect = image.get_rect()
            image_rect.center = (button_x + 40, button_y + 40)

            self.screen.blit(image, image_rect.topleft)
            pygame.draw.rect(self.screen, (0, 0, 0), (button_x, button_y, 80, 80), 2)

        pygame.display.update()

        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    for i, (piece_type, _) in enumerate(piece_options):
                        button_x = box_x + i * 80
                        button_y = box_y
                        if button_x <= mouse_x <= button_x + 80 and button_y <= mouse_y <= button_y + 80:
                            self.promote_pawn(target_coord, piece_type)
                            selecting = False
                            break
                        
    def promote_pawn(self, target_coord, new_piece_type):
        new_piece = Piece(self.selected_piece.color, new_piece_type, self.square_size, self.square_size)
        self.board.representation[target_coord] = new_piece
        self.selected_piece = None
        self.legal_moves = None