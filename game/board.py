from typing import Dict, Tuple, Optional
import pygame
from game.piece import Piece, PieceType, PieceColor
from utils.gameobject import GameObject

class Board(GameObject):
    def __init__(self, columns, rows, light_cell_color, dark_cell_color, square_size, screen):
        self.columns: int = columns
        self.rows: int = rows
        self.light_cell_color: Tuple[int, int, int] = light_cell_color
        self.dark_cell_color: Tuple[int, int, int] = dark_cell_color
        self.square_size: int = square_size
        self.representation: Dict[Tuple[int, int], Piece] = {}
        self.screen = screen
        self.setup_initial_board()
        
    def setup_initial_board(self):
        self.representation.update({
            (0, 0): Piece(PieceColor.BLACK, PieceType.ROOK, self.square_size, self.square_size),
            (1, 0): Piece(PieceColor.BLACK, PieceType.KNIGHT, self.square_size, self.square_size),
            (2, 0): Piece(PieceColor.BLACK, PieceType.BISHOP, self.square_size, self.square_size),
            (3, 0): Piece(PieceColor.BLACK, PieceType.QUEEN, self.square_size, self.square_size),
            (4, 0): Piece(PieceColor.BLACK, PieceType.KING, self.square_size, self.square_size),
            (5, 0): Piece(PieceColor.BLACK, PieceType.BISHOP, self.square_size, self.square_size),
            (6, 0): Piece(PieceColor.BLACK, PieceType.KNIGHT, self.square_size, self.square_size),
            (7, 0): Piece(PieceColor.BLACK, PieceType.ROOK, self.square_size, self.square_size),
            (0, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            (1, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            (2, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            (3, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            (4, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            (5, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            (6, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            (7, 1): Piece(PieceColor.BLACK, PieceType.PAWN, self.square_size, self.square_size),
            
            (0, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (1, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (2, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (3, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (4, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (5, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (6, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (7, 6): Piece(PieceColor.WHITE, PieceType.PAWN, self.square_size, self.square_size),
            (0, 7): Piece(PieceColor.WHITE, PieceType.ROOK, self.square_size, self.square_size),
            (1, 7): Piece(PieceColor.WHITE, PieceType.KNIGHT, self.square_size, self.square_size),
            (2, 7): Piece(PieceColor.WHITE, PieceType.BISHOP, self.square_size, self.square_size),
            (3, 7): Piece(PieceColor.WHITE, PieceType.QUEEN, self.square_size, self.square_size),
            (4, 7): Piece(PieceColor.WHITE, PieceType.KING, self.square_size, self.square_size),
            (5, 7): Piece(PieceColor.WHITE, PieceType.BISHOP, self.square_size, self.square_size),
            (6, 7): Piece(PieceColor.WHITE, PieceType.KNIGHT, self.square_size, self.square_size),
            (7, 7): Piece(PieceColor.WHITE, PieceType.ROOK, self.square_size, self.square_size),
        })
        
    @staticmethod
    def is_light(row, col):
        light = True
        if (row % 2 == 0) and (col % 2 != 0):
            light = False
        elif (row % 2 != 0) and (col % 2 == 0):
            light = False
        return light
    
    def draw_board(self):
        for row in range(self.rows):
            for col in range(self.columns):
                light = self.is_light(row, col)
                color = self.light_cell_color if light else self.dark_cell_color
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self):
        for pos, piece in self.representation.items():
            col, row = pos
            piece_rect = piece.image.get_rect()
            x = col * self.square_size + (self.square_size - piece_rect.width) // 2
            y = row * self.square_size + (self.square_size - piece_rect.height) // 2
            piece.draw_piece(self.screen, x, y)
    
    def update(self):
        self.draw_board()
        self.draw_pieces()
    
    def get_piece_on_pos(self, pos: Tuple[int, int]) -> Optional[Piece]:
        if pos in self.representation:
            return self.representation[pos]
        else:
            return None
        