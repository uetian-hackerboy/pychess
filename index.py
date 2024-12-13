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
    board.move("e2", "e4")
    board.move("b1", "c3")
    while run:
        board.draw_board()
        board.draw_pieces()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # board.draw_board()
        pygame.display.update()
        
    pygame.quit()
    
main()