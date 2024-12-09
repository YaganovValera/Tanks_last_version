import pygame


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)  # Цвет для земли или препятствий
GRAY = (169, 169, 169)  # Цвет для стен

# Размер окна
WIDTH, HEIGHT = 650, 500

CELL_SIZE = 20  # Размер клетки

# Обозначение полей
POLE_EMPTY = 0
POLE_BETON = 1
POLE_KIRPICH = 2
POLE_VRAGS = 3
POLE_WATER = 4
POLE_BONUS = 5
POLE_BASE = 6
POLE_PLAYER = 7
POLE_DBASE = 8


# Отрисовка полей
IMG_POLE_EMPTY = pygame.image.load('images/fs.png')
IMG_POLE_KIRPICH = pygame.image.load('images/kir.png')
IMG_POLE_BETON = pygame.image.load('images/beton.png')
IMG_POLE_BASE = pygame.image.load('images/base.png')
IMG_POLE_DBASE = pygame.image.load('images/dbase.png')
IMG_POLE_WATER = pygame.image.load('images/water.png')
IMG_BULLET = pygame.image.load('images/ammo.png')
IMG_POLE_PLAYER = pygame.image.load('images/ggu.png')
IMG_POLE_VRAG_ST = pygame.image.load('images/vrag1.png')
IMG_POLE_VRAG_LT = pygame.image.load('images/vrag2.png')
IMG_POLE_VRAG_T = pygame.image.load('images/vrag3.png')
IMG_E = pygame.image.load('images/e.png')
IMG_POLE_BONUS = pygame.image.load('images/bzvezdochka.png')

WINNING_SCORE = 1000

