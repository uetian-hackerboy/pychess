from typing import List, Tuple
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
        self.board = None
    
    def increment_num_of_moves(self):
        self.number_of_moves += 1
         
    def get_legal_moves(self, current_coord, representation):
        legal_coords: List[Tuple[int, int]] = []
        self.board = globals.game_instance.board
        col, row = current_coord
        if self.name == PieceType.PAWN:
            increment = row - 1 if self.color == PieceColor.WHITE else row + 1
            increment_two = row - 2 if self.color == PieceColor.WHITE else row + 2
            if self.number_of_moves == 0:
                legal_coords.append((col, increment))
                if not representation.get((col, increment), None):
                    legal_coords.append((col, increment_two))
            else:
                legal_coords.append((col, increment))
            legal_coords = [(c, r) for c, r in legal_coords if not representation.get((c, r), None)]
            diagonal_offsets = [1, -1]
            for offset in diagonal_offsets:
                diagonal_coord = (col + offset , increment)
                piece_at_diagonal_coord: Piece = representation.get(diagonal_coord, None)
                if piece_at_diagonal_coord and piece_at_diagonal_coord.color != self.color:
                    legal_coords.append(diagonal_coord)
                side_coord = (col + offset , row)
                piece_at_side_coord : Piece = representation.get(side_coord, None)
                if piece_at_side_coord and piece_at_side_coord.name == PieceType.PAWN and piece_at_side_coord.color != self.color and piece_at_side_coord.number_of_moves == 1 and (row == 3 or row == 4):
                    legal_coords.append((col + offset, increment))
                    
        elif self.name == PieceType.KNIGHT:
            offsets: List[Tuple[int, int]] = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
            for offset in offsets:
                col_offset, row_offset = offset
                new_coord = (col + col_offset, row + row_offset)
                piece_at_coord = representation.get(new_coord, None)
                if piece_at_coord is None or piece_at_coord.color != self.color:
                    legal_coords.append(new_coord)
        
        elif self.name == PieceType.BISHOP:
            directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            for col_offset, row_offset in directions:
                self.add_legal_moves_in_direction(col, row, col_offset, row_offset, legal_coords, representation)

        elif self.name == PieceType.ROOK:
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            for col_offset, row_offset in directions:
                self.add_legal_moves_in_direction(col, row, col_offset, row_offset, legal_coords, representation)

        elif self.name == PieceType.QUEEN:
            directions = [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
            for col_offset, row_offset in directions:
                self.add_legal_moves_in_direction(col, row, col_offset, row_offset, legal_coords, representation)

        elif self.name == PieceType.KING :
            offsets: List[Tuple[int, int]] = [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
            for offset in offsets:
                col_offset, row_offset = offset
                new_coord = (col + col_offset, row + row_offset)
                piece_at_coord = representation.get(new_coord, None)
                if piece_at_coord is None or piece_at_coord.color != self.color:
                    legal_coords.append(new_coord)
                    
            if self.number_of_moves == 0:
                right_pieces = []
                left_pieces = []
                for i in range(1, 5):
                    right_coord = (col + i, row)
                    left_coord = (col - i, row)
                    right_piece = representation.get(right_coord, None)
                    if right_piece is not None:
                        right_pieces.append(right_piece)
                    left_piece = representation.get(left_coord, None)
                    if left_piece is not None:
                        left_pieces.append(left_piece)
                if len(right_pieces) == 1:
                    if right_pieces[0].name == PieceType.ROOK and right_pieces[0].number_of_moves == 0:
                        legal_coords.append((col + 2, row))
                if len(left_pieces) == 1:
                    if left_pieces[0].name == PieceType.ROOK and left_pieces[0].number_of_moves == 0:
                        legal_coords.append((col - 2, row))   

        legal_coords = [(c, r) for c, r in legal_coords if 0 <= c <= 7 and 0 <= r <= 7]
        return legal_coords

    def add_legal_moves_in_direction(self, col, row, col_offset, row_offset, legal_coords, representation):
        new_coord = (col + col_offset, row + row_offset)
        if 0 <= new_coord[0] <= 7 and 0 <= new_coord[1] <= 7:
            piece_at_coord = representation.get(new_coord, None)
            if piece_at_coord is None:
                legal_coords.append(new_coord)
                self.add_legal_moves_in_direction(new_coord[0], new_coord[1], col_offset, row_offset, legal_coords, representation)
            elif piece_at_coord.color != self.color:
                legal_coords.append(new_coord)
        else:
            return