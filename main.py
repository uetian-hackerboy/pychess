import pygame
from game.game import Game

def main():
    pygame.init()

    screen_width = 640
    screen_height = 640
    square_size = screen_width // 8
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PyChess")

    game = Game(screen, square_size)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()