import random
from collections import defaultdict
from game.piece import PieceType, PieceColor

class Zobrist:
    def __init__(self, board):
        self.board = board
        self.hash_table = defaultdict(int)
        self.zobrist_keys = {}
        self.generate_zobrist_keys()

    def generate_zobrist_keys(self):
        for col in range(8):
            for row in range(8):
                for piece in PieceType:
                    for color in PieceColor:
                        self.zobrist_keys[(col, row, piece, color)] = random.getrandbits(64)

    def compute_hash(self):
        hash_value = 0
        for (coord, piece) in self.board.representation.items():
            col, row = coord
            if piece:
                hash_value ^= self.zobrist_keys[(col, row, piece.name, piece.color)]
        return hash_value

    def update_history(self, current_hash):
        self.hash_table[current_hash] += 1
        return self.hash_table[current_hash]

    def reset_history(self):
        self.hash_table.clear()