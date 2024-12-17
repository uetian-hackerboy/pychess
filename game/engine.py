from game.board import Board
from game.piece import PieceColor, Piece, PieceType
import random
import globals

class Engine:
    def __init__(self, board: Board, ai_color: PieceColor):
        self.board = board
        self.ai_color = ai_color

    def make_move(self):
        all_legal_moves = self.get_all_legal_moves()
        if not all_legal_moves:
            return  

        move = random.choice(all_legal_moves)

        piece, start_pos, end_pos = move
        self.execute_move(piece, start_pos, end_pos)

    def get_all_legal_moves(self):
        game = globals.game_instance
        legal_moves = []
        for pos, piece in game.board.representation.items():
            if piece.color == self.ai_color:
                moves = piece.get_legal_moves(pos, game.board.representation)
                for move in moves:
                    if not game.king_will_be_in_danger(game.board.representation, pos, piece, move, self.ai_color):
                        legal_moves.append((piece, pos, move))
        print("LegalMoves",len(legal_moves))
        return legal_moves

    def execute_move(self, piece: Piece, start_pos, end_pos):
        del self.board.representation[start_pos]
        self.board.representation[end_pos] = piece
        piece.increment_num_of_moves()