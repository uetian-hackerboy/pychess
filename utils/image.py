import pygame
    
def load_image(image_path, image_width, image_height, scale_factor=0.8):
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

def draw_image(image, screen, x_coord, y_coord):
    screen.blit(image, (x_coord, y_coord))