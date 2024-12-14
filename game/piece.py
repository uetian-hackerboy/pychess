from typing import List, Tuple
import pygame
from enum import Enum
import globals
from utils.image import load_image
class PieceType(Enum):
    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"

class PieceColor(Enum):
    WHITE = "white"
    BLACK = "black"

class Piece:
    def __init__(self, color: PieceColor, name: PieceType, image_width: int, image_height: int):
        self.color = color
        self.name = name
        self.image_width = image_width
        self.image_height = image_height
        self.number_of_moves = 0
        self.image = load_image(f"assets/{color.value}_{name.value}.png", image_width=image_width, image_height=image_height)
    
    def increment_num_of_moves(self):
        self.number_of_moves += 1
         
    def get_legal_moves(self, current_coord):
        legal_coords: List[Tuple[int, int]] = []
        board = globals.game_instance.board
        col, row = current_coord
        if self.name == PieceType.PAWN:
            if self.color == PieceColor.WHITE:
                if self.number_of_moves == 0:
                    legal_coords.append((col, row - 1))
                    legal_coords.append((col, row - 2))
                else:
                    legal_coords.append((col, row - 1))
                legal_coords = [(c, r) for c, r in legal_coords if not board.representation.get((c, r), None)]
                right_diagonal_coord = (col + 1, row - 1)
                piece_at_coord = board.representation.get(right_diagonal_coord, None)
                if piece_at_coord is not None:
                    legal_coords.append(right_diagonal_coord)
                left_diagonal_coord = (col - 1, row - 1)
                piece_at_coord = board.representation.get(left_diagonal_coord, None)
                if piece_at_coord and piece_at_coord.color != self.color:
                    legal_coords.append(left_diagonal_coord)
            else:
                if self.number_of_moves == 0:
                    legal_coords.append((col, row + 1))
                    legal_coords.append((col, row + 2))
                else:
                    legal_coords.append((col, row + 1))
                legal_coords = [(c, r) for c, r in legal_coords if not board.representation.get((c, r), None)]
                right_diagonal_coord = (col + 1, row + 1)
                piece_at_coord = board.representation.get(right_diagonal_coord, None)
                if piece_at_coord is not None:
                    legal_coords.append(right_diagonal_coord)
                left_diagonal_coord = (col - 1, row + 1)
                piece_at_coord = board.representation.get(left_diagonal_coord, None)
                if piece_at_coord and piece_at_coord.color != self.color:
                    legal_coords.append(left_diagonal_coord)
        
        elif self.name == PieceType.KNIGHT:
            offsets: List[Tuple[int, int]] = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
            for offset in offsets:
                col_offset, row_offset = offset
                new_coord = (col + col_offset, row + row_offset)
                piece_at_coord = board.representation.get(new_coord, None)
                if piece_at_coord is None or piece_at_coord.color != self.color:
                    legal_coords.append(new_coord)
        
        elif self.name == PieceType.BISHOP:
            def add_legal_moves_in_direction(col, row, col_offset, row_offset):
                new_coord = (col + col_offset, row + row_offset)
                if 0 <= new_coord[0] <= 7 and 0 <= new_coord[1] <= 7:
                    piece_at_coord = board.representation.get(new_coord, None)
                    if piece_at_coord is None:
                        legal_coords.append(new_coord)
                        add_legal_moves_in_direction(new_coord[0], new_coord[1], col_offset, row_offset)
                    elif piece_at_coord.color != self.color:
                        legal_coords.append(new_coord)
                else:
                    return
            directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            for col_offset, row_offset in directions:
                add_legal_moves_in_direction(col, row, col_offset, row_offset)

        elif self.name == PieceType.ROOK:
            def add_legal_moves_in_direction(col, row, col_offset, row_offset):
                new_coord = (col + col_offset, row + row_offset)
                if 0 <= new_coord[0] <= 7 and 0 <= new_coord[1] <= 7:
                    piece_at_coord = board.representation.get(new_coord, None)
                    if piece_at_coord is None:
                        legal_coords.append(new_coord)
                        add_legal_moves_in_direction(new_coord[0], new_coord[1], col_offset, row_offset)
                    elif piece_at_coord.color != self.color:
                        legal_coords.append(new_coord)
                else:
                    return
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for col_offset, row_offset in directions:
                add_legal_moves_in_direction(col, row, col_offset, row_offset)

        elif self.name == PieceType.QUEEN:
            def add_legal_moves_in_direction(col, row, col_offset, row_offset):
                new_coord = (col + col_offset, row + row_offset)
                if 0 <= new_coord[0] <= 7 and 0 <= new_coord[1] <= 7:
                    piece_at_coord = board.representation.get(new_coord, None)
                    if piece_at_coord is None:
                        legal_coords.append(new_coord)
                        add_legal_moves_in_direction(new_coord[0], new_coord[1], col_offset, row_offset)
                    elif piece_at_coord.color != self.color:
                        legal_coords.append(new_coord)
                else:
                    return
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
            for col_offset, row_offset in directions:
                add_legal_moves_in_direction(col, row, col_offset, row_offset)

        elif self.name == PieceType.KING:
            offsets: List[Tuple[int, int]] = [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
            for offset in offsets:
                col_offset, row_offset = offset
                new_coord = (col + col_offset, row + row_offset)
                piece_at_coord = board.representation.get(new_coord, None)
                if piece_at_coord is None or piece_at_coord.color != self.color:
                    legal_coords.append(new_coord)
        
        legal_coords = [(c, r) for c, r in legal_coords if 0 <= c <= 7 and 0 <= r <= 7]
        return legal_coords