import pygame
from source.board import Board

pygame.init()


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyChess")

SQUARE_SIZE = SCREEN_WIDTH // 8

def main():
    run = True
    board = Board(columns=8, rows=8, light_cell_color=(232,237,249), dark_cell_color=(183,192,216), square_size=SQUARE_SIZE, screen=screen)
    selected_coord = None
    selected_piece = None
    dragging = False
    while run:
        board.draw_board()
        board.draw_pieces()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                selected_coord = (col, row)
                if selected_coord:
                    selected_piece = board.representation[selected_coord]
                    del[board.representation[selected_coord]]
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                    board.representation[(col, row)] = selected_piece
                    dragging = False
                    selected_piece = None
        if dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            piece_image = selected_piece.image
            piece_rect = piece_image.get_rect()
            x = piece_rect.width // 2
            y = piece_rect.height // 2
            piece_rect.topleft = (mouse_x - x, mouse_y - y)
            screen.blit(piece_image, piece_rect.topleft)
        pygame.display.update()
        
    pygame.quit()
    
main()