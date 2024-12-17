from game.board import Board
from game.piece import PieceColor, Piece, PieceType
import globals
import math

class Engine:
    def __init__(self, board: Board, ai_color: PieceColor):
        self.board = board
        self.ai_color = ai_color
        self.piece_values = {
            PieceType.PAWN: 100,
            PieceType.KNIGHT: 320,
            PieceType.BISHOP: 330,
            PieceType.ROOK: 500,
            PieceType.QUEEN: 900,
            PieceType.KING: 0
        }
        self.transposition_table = {}

        self.piece_square_tables = {
            PieceType.PAWN: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            PieceType.KNIGHT: [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],
            PieceType.BISHOP: [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],
            PieceType.ROOK: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0]
            ],
            PieceType.QUEEN: [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ],
            PieceType.KING: [
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20]
            ]
        }

    def make_move(self):
        legal_moves = self.get_all_legal_moves()
        capture_moves = [move for move in legal_moves if self.is_capture(move)]
        if capture_moves:
            best_capture_move = self.choose_best_capture(capture_moves)
            piece, start_pos, end_pos = best_capture_move
        else:
            _, best_move = self.minimax(self.board, 3, -math.inf, math.inf, True)
            if best_move:
                piece, start_pos, end_pos = best_move
        self.execute_move(piece, start_pos, end_pos)

    def is_capture(self, move):
        _, _, end_pos = move
        captured_piece = self.board.representation.get(end_pos)
        return captured_piece and captured_piece.color != self.ai_color
    
    def choose_best_capture(self, capture_moves):
        capture_evaluations = []
        for move in capture_moves:
            piece, start_pos, end_pos = move
            captured_piece = self.board.representation.get(end_pos)
            self.execute_move(piece, start_pos, end_pos)
            board_eval = self.evaluate_board()
            self.undo_move(piece, start_pos, end_pos, captured_piece)
            capture_evaluations.append((board_eval, move))
        sorted_capture_moves = sorted(capture_evaluations, key=lambda x: -x[0])
        return sorted_capture_moves[0][1]

    def order_moves(self, legal_moves):
        ordered_moves = []
        for move in legal_moves:
            piece, _, end_pos = move
            captured_piece = self.board.representation.get(end_pos)
            capture_value = self.piece_values.get(captured_piece.name, 0) if captured_piece else 0
            if capture_value > 0:
                ordered_moves.append((capture_value + 1000, move))  
            else:
                ordered_moves.append((0, move))
        return [move for _, move in sorted(ordered_moves, key=lambda x: -x[0])]


    def get_all_legal_moves(self):
        game = globals.game_instance
        legal_moves = []
        for pos, piece in game.board.representation.items():
            if piece.color == self.ai_color:
                moves = piece.get_legal_moves(pos, game.board.representation)
                for move in moves:
                    if not game.king_will_be_in_danger(game.board.representation, pos, piece, move, self.ai_color):
                        legal_moves.append((piece, pos, move))
        return legal_moves

    def execute_move(self, piece: Piece, start_pos, end_pos):
        del self.board.representation[start_pos]
        self.board.representation[end_pos] = piece
        piece.increment_num_of_moves()

    def evaluate_board(self):
        score = 0
        for pos, piece in self.board.representation.items():
            piece_value = self.piece_values.get(piece.name, 0)
            table = self.piece_square_tables.get(piece.name, [[0]*8 for _ in range(8)])
            row, col = pos

            if piece.color == PieceColor.WHITE:
                score += piece_value + table[row][col]
            else:
                score -= piece_value + table[7 - row][col]

            
            captured_piece = self.board.representation.get(pos)
            if captured_piece:
                captured_value = self.piece_values.get(captured_piece.name, 0)
                score += captured_value if piece.color == PieceColor.WHITE else -captured_value
        return score

    def minimax(self, board: Board, depth, alpha, beta, maximizing_player):
        board_hash = hash(frozenset(board.representation.items()))
        if board_hash in self.transposition_table and self.transposition_table[board_hash]["depth"] >= depth:
            return self.transposition_table[board_hash]["evaluation"], self.transposition_table[board_hash]["best_move"]
        if depth == 0:
            evaluation = self.evaluate_board()
            self.transposition_table[board_hash] = {"evaluation": evaluation, "best_move": None, "depth": depth}
            return evaluation, None
        legal_moves = self.order_moves(self.get_all_legal_moves())
        if not legal_moves:
            evaluation = self.evaluate_board()
            return evaluation, None
        best_move = None
    
        if maximizing_player:
            max_eval = -math.inf
            for move in legal_moves:
                piece, start_pos, end_pos = move
                captured_piece = board.representation.get(end_pos)
                self.execute_move(piece, start_pos, end_pos)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                self.undo_move(piece, start_pos, end_pos, captured_piece)
    
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_hash] = {"evaluation": max_eval, "best_move": best_move, "depth": depth}
            return max_eval, best_move
    
        else:
            min_eval = math.inf
            for move in legal_moves:
                piece, start_pos, end_pos = move
                captured_piece = board.representation.get(end_pos)
                self.execute_move(piece, start_pos, end_pos)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                self.undo_move(piece, start_pos, end_pos, captured_piece)
    
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                
            self.transposition_table[board_hash] = {"evaluation": min_eval, "best_move": best_move, "depth": depth}
            return min_eval, best_move


    def undo_move(self, piece: Piece, start_pos, end_pos, captured_piece):
        self.board.representation[start_pos] = piece
        if captured_piece:
            self.board.representation[end_pos] = captured_piece
        else:
            del self.board.representation[end_pos]
        piece.decrement_num_of_moves()