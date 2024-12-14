import pygame
from enum import Enum

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
        self.image = self.load_image(f"assets/{color.value}_{name.value}.png", image_width=image_width, image_height=image_height)
    
    def load_image(self, image_path, image_width, image_height, scale_factor=0.8):
        image = pygame.image.load(image_path).convert_alpha()
        original_width, original_height = image.get_size()
    
        aspect_ratio = original_width / original_height

        if image_width / image_height > aspect_ratio:
            new_height = int(image_height * scale_factor)
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = int(image_width * scale_factor)
            new_height = int(new_width / aspect_ratio)

        return pygame.transform.smoothscale(image, (new_width, new_height))
    
    def draw_piece(self, screen, x_coord, y_coord):
        screen.blit(self.image, (x_coord, y_coord))