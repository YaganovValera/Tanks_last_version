import random
import pygame
import Class_Bullet
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
    def __init__(self, tank_type, row, col, base_position, field, shoot_interval=1000):
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
        self.hp = TANK_STATS[tank_type]['hp']
        self.damage = TANK_STATS[tank_type]['damage']
        self.bullets = []
        self.shoot_interval = shoot_interval  # Интервал между выстрелами (в миллисекундах)
        self.last_shot_time = pygame.time.get_ticks()  # Время последнего выстрела

    def move_towards_base(self):
        """Двигается к базе игрока, избегая бетонных стен."""
        if self.moving:
            return

        self.shoot()

        row, col = self.row, self.col
        target_row, target_col = self.base_position

        # Проверяем клетку перед танком
        direction_offsets = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }
        if self.direction in direction_offsets:
            offset_row, offset_col = direction_offsets[self.direction]
            forward_row, forward_col = row + offset_row, col + offset_col

            if 0 <= forward_row < self.field.rows and 0 <= forward_col < self.field.cols:
                forward_cell = self.field.level_matrix[forward_row][forward_col]

                if forward_cell == POLE_BASE:
                    # Если перед танком база, останавливаемся и стреляем
                    self.moving = False
                    self.shoot()
                    return
                elif forward_cell == POLE_KIRPICH:
                    # Если перед танком кирпич, стреляем в него
                    self.shoot()
                    return

        # Возможные движения: вниз, вверх, вправо, влево
        possible_moves = [
            (row + 1, col, 'DOWN'),
            (row - 1, col, 'UP'),
            (row, col + 1, 'RIGHT'),
            (row, col - 1, 'LEFT')
        ]

        # Исключаем возврат на предыдущую позицию
        valid_moves = [
            (new_row, new_col, direction)
            for new_row, new_col, direction in possible_moves
            if self.can_move(new_row, new_col)
        ]

        if valid_moves:
            # Сортируем движения по расстоянию до цели (базы)
            valid_moves.sort(key=lambda move: abs(move[0] - target_row) + abs(move[1] - target_col))

            # Берем наилучший ход
            new_row, new_col, new_direction = valid_moves[0]

            # Устанавливаем направление танка
            self.direction = new_direction

            # Обновляем цель движения
            self.target_x, self.target_y = new_col * CELL_SIZE, new_row * CELL_SIZE
            self.row, self.col = new_row, new_col
            self.moving = True
        else:
            # Если движение невозможно, остаемся на месте
            self.moving = False

    def can_move(self, row, col):
        """Проверка, можно ли двигаться на указанную клетку."""
        # Преобразуем row и col в целые числа
        row, col = int(row), int(col)
        if 0 <= row < self.field.rows and 0 <= col < self.field.cols:
            cell_value = self.field.level_matrix[row][col]
            if cell_value not in [POLE_BETON, POLE_WATER, POLE_KIRPICH, POLE_BASE]:
                return True
        return False

    def move(self):
        """Плавное движение танка к целевой позиции."""
        if self.moving:
            self.x = self.approach(self.x, self.target_x)
            self.y = self.approach(self.y, self.target_y)

            # Приведение координат к целым числам
            self.x = int(self.x)
            self.y = int(self.y)

            # Проверяем, достиг ли танк целевой позиции
            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False

    def approach(self, current, target):
        """Плавное движение к целевой позиции."""
        if current < target:
            return min(current + self.speed, target)
        elif current > target:
            return max(current - self.speed, target)
        return current

    def shoot(self):
        """Танк стреляет одной пулей с заданным интервалом."""
        if pygame.time.get_ticks() - self.last_shot_time < self.shoot_interval:
            return

        # Стреляем
        directions = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0),
        }

        if self.direction in directions:
            dx, dy = directions[self.direction]

            bullet_x = self.x + dx
            bullet_y = self.y + dy
            bullet = Class_Bullet.Bullet(bullet_x, bullet_y, self.direction, self.damage)
            self.bullets.append(bullet)

        self.last_shot_time = pygame.time.get_ticks()

    def update(self, player_tank):
        """Обновление состояния танка."""
        self.move()
        if not self.moving:
            self.move_towards_base()

        # Приведение координат пуль к целым числам
        for bullet in self.bullets[:]:
            bullet.update(self.field, player_tank, None)
            if not bullet.active:
                self.bullets.remove(bullet)

    def draw(self, screen):
        """
        Отрисовывает танк на экране.
        """
        direction_angles = {'UP': 0, 'DOWN': 180, 'LEFT': 90, 'RIGHT': -90}
        rotated_image = pygame.transform.rotate(self.image, direction_angles[self.direction])
        screen.blit(rotated_image, (self.x, self.y))

        # Отрисовываем снаряды
        for bullet in self.bullets:
            bullet.draw(screen)


class BotManager:
    def __init__(self, field):
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
        spawn_positions = [
            (row, col) for row in range(self.field.rows)
            for col in range(self.field.cols)
            if self.field.level_matrix[row][col] == POLE_VRAGS
        ]
        for spawn in spawn_positions:
            tank_type = random.choice(['ТТ', 'СТ', 'ЛТ'])  # Случайный выбор танка
            bot = TankEnemy(tank_type, spawn[0], spawn[1], self.base_position, self.field)
            self.enemies.append(bot)

    def update(self, player_tank):
        for bot in self.enemies:
            bot.update(player_tank)

    def draw(self, screen):
        for bot in self.enemies:
            bot.draw(screen)
