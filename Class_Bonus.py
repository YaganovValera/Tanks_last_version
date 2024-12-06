import random

from CONST import *

# в секундах
BONUS_LIFETIME = 30
BONUS_RESPAWN_TIME = 5


class Bonus:
    def __init__(self, field):
        """
        Конструктор для бонуса.
        :param field: объект класса Field, чтобы взаимодействовать с картой.
        """
        self.field = field
        self.position = None                            # Текущая позиция бонуса (строка, столбец)
        self.spawn_time = pygame.time.get_ticks()       # Время появления бонуса
        self.active = False                             # Флаг, указывающий, активен ли бонус на карте

    def spawn(self):
        """
        Создание бонуса в случайной пустой клетке.
        """
        empty_cells = [
            (row, col)
            for row in range(self.field.rows)
            for col in range(self.field.cols)
            if self.field.level_matrix[row][col] == POLE_EMPTY
        ]

        if empty_cells:
            self.position = random.choice(empty_cells)
            self.field.level_matrix[self.position[0]][self.position[1]] = POLE_BONUS
            self.spawn_time = pygame.time.get_ticks()
            self.active = True

    def update(self):
        """
        Проверка состояния бонуса:
        - Если бонус не активен, проверяем, прошли ли 10 секунд с последнего появления.
        - Если бонус активен и прошло 15 секунд, бонус исчезает.
        """
        current_time = pygame.time.get_ticks()

        # Если бонус не активен, проверяем необходимость создания
        if not self.active and current_time - self.spawn_time >= BONUS_RESPAWN_TIME * 1000:
            self.spawn()

        # Если бонус активен и истекло время его жизни
        if self.active and current_time - self.spawn_time >= BONUS_LIFETIME * 1000:
            self.remove()

    def remove(self):
        """
        Удаление бонуса с карты.
        """
        if self.position:
            self.field.level_matrix[self.position[0]][self.position[1]] = 0
        self.position = None
        self.spawn_time = pygame.time.get_ticks()
        self.active = False

    def collect(self):
        """
        Сбор бонуса. Вызывается, когда игрок попадает на клетку с бонусом.
        """
        self.remove()
