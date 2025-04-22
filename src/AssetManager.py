import pygame

def load_image(asset_path):
    image = pygame.image.load(f"assets/images/{asset_path}").convert_alpha()
    original_size = image.get_size()
    size = (int(original_size[0] * 2 / 3), int(original_size[1] * 2 / 3))
    image = pygame.transform.smoothscale(image, size)
    return image