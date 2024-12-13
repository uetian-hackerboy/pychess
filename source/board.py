from typing import Tuple
import pygame
from .piece import Piece

class Board:
    def __init__(self, columns, rows, light_cell_color, dark_cell_color, square_size, screen):
        self.columns: int = columns
        self.rows: int = rows
        self.light_cell_color: Tuple[int, int, int] = light_cell_color
        self.dark_cell_color: Tuple[int, int, int] = dark_cell_color
        self.square_size: int = square_size
        self.screen = screen
        self.representation = {
            (0, 0): Piece("black", "rook", self.square_size, self.square_size),
            (1, 0): Piece("black", "knight", self.square_size, self.square_size),
            (2, 0): Piece("black", "bishop", self.square_size, self.square_size),
            (3, 0): Piece("black", "queen", self.square_size, self.square_size),
            (4, 0): Piece("black", "king", self.square_size, self.square_size),
            (5, 0): Piece("black", "bishop", self.square_size, self.square_size),
            (6, 0): Piece("black", "knight", self.square_size, self.square_size),
            (7, 0): Piece("black", "rook", self.square_size, self.square_size),
            (0, 1): Piece("black", "pawn", self.square_size, self.square_size),
            (1, 1): Piece("black", "pawn", self.square_size, self.square_size),
            (2, 1): Piece("black", "pawn", self.square_size, self.square_size),
            (3, 1): Piece("black", "pawn", self.square_size, self.square_size),
            (4, 1): Piece("black", "pawn", self.square_size, self.square_size),
            (5, 1): Piece("black", "pawn", self.square_size, self.square_size),
            (6, 1): Piece("black", "pawn", self.square_size, self.square_size),
            (7, 1): Piece("black", "pawn", self.square_size, self.square_size),
            
            (0, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (1, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (2, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (3, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (4, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (5, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (6, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (7, 6): Piece("white", "pawn", self.square_size, self.square_size),
            (0, 7): Piece("white", "rook", self.square_size, self.square_size),
            (1, 7): Piece("white", "knight", self.square_size, self.square_size),
            (2, 7): Piece("white", "bishop", self.square_size, self.square_size),
            (3, 7): Piece("white", "queen", self.square_size, self.square_size),
            (4, 7): Piece("white", "king", self.square_size, self.square_size),
            (5, 7): Piece("white", "bishop", self.square_size, self.square_size),
            (6, 7): Piece("white", "knight", self.square_size, self.square_size),
            (7, 7): Piece("white", "rook", self.square_size, self.square_size),
        }

        
    def is_light(self, row, col):
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
            
    
    def pos_to_coord(self, pos):
        file = pos[0]
        rank = pos[1]
        col = ord(file) - 97
        row = 8 - int(rank)
        return col, row

    def move(self, start_pos: str, end_pos: str):
        start_coord = self.pos_to_coord(start_pos)
        end_coord = self.pos_to_coord(end_pos)
        print(start_coord)

        if start_coord in self.representation:
            self.representation[end_coord] = self.representation.pop(start_coord)
        else:
            print(f"No piece found at {start_pos}")
