import pygame
from game.board import Board
from utils.gameobject import GameObject
import globals
from game.piece import PieceType, PieceColor

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
            globals.game_instance = self
    
    def update(self):
        return self.board.update()

    def run(self):
        run = True
        while run:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(event.pos)
            if self.dragging:
                self.handle_piece_drag()
            pygame.display.update()
        pygame.quit()

    def handle_mouse_down(self, pos):
        col, row = pos[0] // self.square_size, pos[1] // self.square_size
        self.selected_coord = (col, row)
        self.selected_piece = self.board.get_piece_obj_on_pos(self.selected_coord)
        if self.selected_piece and self.selected_piece.color == self.current_turn:
            self.legal_moves = self.selected_piece.get_legal_moves(self.selected_coord, self.board.representation)
            del[self.board.representation[self.selected_coord]]
            self.dragging = True

    def handle_mouse_up(self, pos):
        if self.dragging:
            col, row = pos[0] // self.square_size, pos[1] // self.square_size
            col_selected, row_selected = self.selected_coord
            if self.legal_moves is not None:
                if not self.king_will_be_in_danger((col, row)):
                    if (col, row) in self.legal_moves:
                        self.selected_piece.increment_num_of_moves()
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
                        if self.current_turn == PieceColor.WHITE:
                            self.current_turn = PieceColor.BLACK
                        else:
                            self.current_turn = PieceColor.WHITE
                    else:
                        self.board.representation[self.selected_coord] = self.selected_piece
                else:
                    self.board.representation[self.selected_coord] = self.selected_piece
            self.dragging = False
            self.selected_piece = None
            self.legal_moves = None

    def king_will_be_in_danger(self, target_coord):
        clone_representation = self.board.representation.copy()
        col, row = target_coord

        if self.selected_coord in clone_representation:
            del clone_representation[self.selected_coord]
        clone_representation[(col, row)] = self.selected_piece

        king_position = None
        for coord, piece in clone_representation.items():
            if piece.name == PieceType.KING and piece.color == self.current_turn:
                king_position = coord
                break

        if not king_position:
            raise ValueError("King is not even on the board bro.")

        opponent = PieceColor.WHITE if self.current_turn == PieceColor.BLACK else PieceColor.BLACK
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