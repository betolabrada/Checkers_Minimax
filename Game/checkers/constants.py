import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (46, 134, 193) # PIEZA
WHITE = (255, 255, 255) # PIEZA
BLACK = (0, 0, 0) # TABLERO (ahora es dark blue)
BLUE = (0, 255, 0) #  PUNTOS
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('Game/assets/crown.png'), (44, 25))
