import random
from CONST import *

TANK_STATS = {
    'ТТ': {'hp': 500, 'damage': 30, 'speed': 1},
    'СТ': {'hp': 300, 'damage': 15, 'speed': 1.5},
    'ЛТ': {'hp': 200, 'damage': 5, 'speed': 2}
}

TANK_IMAGES = {
    'ТТ': IMG_POLE_VRAG_T,      # Тяжелый танк (ТТ)
    'СТ': IMG_POLE_VRAG_ST,     # Средний танк (СТ)
    'ЛТ': IMG_POLE_VRAG_LT      # Легкий танк (ЛТ)
}


class TankEnemy:
    def __init__(self, tank_type, row, col, base_position, field):
        """
        Конструктор для танка.
        :param tank_type: Тип танка (ТТ, СТ, ЛТ)
        :param row: Строка позиции танка.
        :param col: Столбец позиции танка.
        """
        self.tank_type = tank_type
        self.row = row  # Логическая строка
        self.col = col  # Логический столбец
        self.x, self.y = col * CELL_SIZE, row * CELL_SIZE  # Экранные координаты
        self.target_x, self.target_y = self.x, self.y
        self.base_position = base_position
        self.field = field
        self.image = TANK_IMAGES.get(tank_type)
        self.direction = 'DOWN'
        self.moving = False
        self.speed = TANK_STATS[tank_type]['speed']
        self.HP = TANK_STATS[tank_type]['hp']
        self.damage = TANK_STATS[tank_type]['damage']

    def draw(self, screen):
        """
        Отрисовывает танк на экране.
        """
        direction_angles = {'UP': 0, 'DOWN': 180, 'LEFT': 90, 'RIGHT': -90}
        rotated_image = pygame.transform.rotate(self.image, direction_angles[self.direction])
        screen.blit(rotated_image, (self.x, self.y))

    def approach(self, current, target):
        """
        Двигается к целевой координате с учетом скорости.
        """
        if current < target:
            return min(current + self.speed, target)
        elif current > target:
            return max(current - self.speed, target)
        return current

    def move(self):
        """
        Плавное движение танка к целевой позиции.
        """
        if self.moving:
            self.x = self.approach(self.x, self.target_x)
            self.y = self.approach(self.y, self.target_y)

            # Проверяем, достиг ли танк целевой позиции
            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False

    def move_towards_base(self):
        """
        Двигается к базе игрока, избегая бетонных стен.
        """
        if self.moving:
            return  # Дождаться окончания текущего движения

        row, col = self.row, self.col
        target_row, target_col = self.base_position

        # Определяем направление движения
        new_row, new_col = row, col
        if row < target_row:  # Движение вниз
            new_row += 1
            self.direction = 'DOWN'
        elif row > target_row:  # Движение вверх
            new_row -= 1
            self.direction = 'UP'
        elif col < target_col:  # Движение вправо
            new_col += 1
            self.direction = 'RIGHT'
        elif col > target_col:  # Движение влево
            new_col -= 1
            self.direction = 'LEFT'

        # Проверяем, можно ли переместиться на новую позицию
        if 0 <= new_row < self.field.rows and 0 <= new_col < self.field.cols:
            if self.field.level_matrix[new_row][new_col] in [POLE_EMPTY, POLE_BASE]:
                self.row, self.col = new_row, new_col
                self.target_x, self.target_y = new_col * CELL_SIZE, new_row * CELL_SIZE
                self.moving = True

    def update(self):
        """
        Обновление состояния танка (движение к базе).
        """
        self.move()
        if not self.moving:
            self.move_towards_base()


class BotManager:
    def __init__(self, field):
        """
        Менеджер ботов.
        :param field: поле, на котором находятся боты
        """
        self.field = field
        self.base_position = self.get_base_position()
        self.enemies = []
        self.spawn_bots()

    def get_base_position(self):
        for row in range(self.field.rows):
            for col in range(self.field.cols):
                if self.field.level_matrix[row][col] == POLE_BASE:
                    return (row, col)

    def spawn_bots(self):
        """
        Спавн ботов на случайных позициях.
        Количество ботов должно быть равно числу спавнов (POLE_VRAGS).
        """
        spawn_positions = [
            (row, col) for row in range(self.field.rows)
            for col in range(self.field.cols)
            if self.field.level_matrix[row][col] == POLE_VRAGS
        ]

        for spawn in spawn_positions:
            tank_type = random.choice(['ТТ', 'СТ', 'ЛТ'])  # Случайный выбор танка
            bot = TankEnemy(tank_type, spawn[0], spawn[1], self.base_position, self.field)
            self.enemies.append(bot)

    def update(self):
        """
        Обновление состояния всех ботов.
        Пока что без логики, только отрисовка.
        """
        for bot in self.enemies:
            bot.update()

    def draw(self, screen):
        """
        Отрисовывает всех ботов на экране.
        """
        for bot in self.enemies:
            bot.draw(screen)
