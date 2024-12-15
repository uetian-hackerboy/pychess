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
        if self.selected_piece:
            self.legal_moves = self.selected_piece.get_legal_moves(self.selected_coord)
            del[self.board.representation[self.selected_coord]]
            self.dragging = True

    def handle_mouse_up(self, pos):
        if self.dragging:
            col, row = pos[0] // self.square_size, pos[1] // self.square_size
            if self.legal_moves is not None:
             if (col, row) in self.legal_moves:
                self.selected_piece.increment_num_of_moves()
                if self.selected_piece.name == PieceType.KING and self.selected_coord == (4,row):
                   if col == 6  :
                    self.board.representation[(5, row)] = self.board.representation[(7,row)]
                    del[self.board.representation[(7, row)]]
                   elif col == 2 :
                    self.board.representation[(3, row)] = self.board.representation[(0,row)]
                    del[self.board.representation[(0, row)]]
                if self.selected_piece.name == PieceType.PAWN:
                    piece_at_target = self.board.representation.get((col, row), None)
                    if piece_at_target is None:
                        col_selected, row_selected = self.selected_coord
                        offset = (col_selected - col, row_selected - row)
                        if self.selected_piece.color == PieceColor.WHITE:
                            if offset == (-1, 1):
                                del[self.board.representation[(col_selected + 1, row_selected)]]
                            if offset == (1, 1):
                                del[self.board.representation[(col_selected - 1, row_selected)]]
                        else:
                            if offset == (-1, -1):
                                del[self.board.representation[(col_selected + 1, row_selected)]]
                            if offset == (1, -1):
                                del[self.board.representation[(col_selected - 1, row_selected)]]
                self.board.representation[(col, row)] = self.selected_piece
             else:
                self.board.representation[self.selected_coord] = self.selected_piece
             self.dragging = False
             self.selected_piece = None
             self.legal_moves = None
                

    def handle_piece_drag(self):
         if self.selected_piece is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            piece_image = self.selected_piece.image
            piece_rect = piece_image.get_rect()
            piece_rect.topleft = (mouse_x - piece_rect.width // 2, mouse_y - piece_rect.height // 2)
            self.screen.blit(piece_image, piece_rect.topleft)