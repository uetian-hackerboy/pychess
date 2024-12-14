import pygame
from game.board import Board
from utils.gameobject import GameObject

class Game(GameObject):
    def __init__(self, screen, square_size):
        self.screen = screen
        self.square_size = square_size
        self.board = Board(columns=8, rows=8, light_cell_color=(232,237,249), dark_cell_color=(183,192,216), square_size=square_size, screen=screen)
        self.selected_piece = None
        self.selected_coord = None
        self.dragging = False
    
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
        """Handle mouse click event."""
        col, row = pos[0] // self.square_size, pos[1] // self.square_size
        self.selected_coord = (col, row)
        self.selected_piece = self.board.get_piece_on_pos(self.selected_coord)
        if self.selected_piece:
            del[self.board.representation[self.selected_coord]]
            self.dragging = True

    def handle_mouse_up(self, pos):
        """Handle mouse release event."""
        if self.dragging:
            col, row = pos[0] // self.square_size, pos[1] // self.square_size
            self.board.representation[(col, row)] = self.selected_piece
            self.dragging = False
            self.selected_piece = None

    def handle_piece_drag(self):
        """Drag the piece while the mouse is down."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        piece_image = self.selected_piece.image
        piece_rect = piece_image.get_rect()
        piece_rect.topleft = (mouse_x - piece_rect.width // 2, mouse_y - piece_rect.height // 2)
        self.screen.blit(piece_image, piece_rect.topleft)