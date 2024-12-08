import random
import Class_Bullet
from CONST import *

TANK_STATS = {
    'ТТ': {'hp': 300, 'damage': 30, 'speed': 1, 'get_score': 200},
    'СТ': {'hp': 150, 'damage': 15, 'speed': 1.25, 'get_score': 100},
    'ЛТ': {'hp': 100, 'damage': 5, 'speed': 1.5, 'get_score': 50}
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
        self.get_score = TANK_STATS[tank_type]['get_score']
        self.bullets = []
        self.shoot_interval = shoot_interval  # Интервал между выстрелами (в миллисекундах)
        self.last_shot_time = pygame.time.get_ticks()  # Время последнего выстрела
        self.recent_positions = []

    def move_towards_base(self, player_tank):
        """Двигается к базе игрока, избегая препятствий."""
        if self.moving:
            return

        self.shoot()

        row, col = self.row, self.col
        target_row, target_col = self.base_position

        # Возможные движения: вниз, вверх, вправо, влево
        possible_moves = [
            (row + 1, col, 'DOWN'),
            (row - 1, col, 'UP'),
            (row, col + 1, 'RIGHT'),
            (row, col - 1, 'LEFT')
        ]

        # Исключаем возврат на недавно посещенные позиции
        valid_moves = [
            (new_row, new_col, direction)
            for new_row, new_col, direction in possible_moves
            if (new_row, new_col) not in self.recent_positions
        ]

        # Если есть валидные ходы, обработать их
        if valid_moves:
            # Сортируем по расстоянию до базы и типу клетки
            valid_moves.sort(key=lambda move: (
                abs(move[0] - target_row) + abs(move[1] - target_col),  # Первичный критерий: расстояние до базы
                self.field.level_matrix[move[0]][move[1]]               # Вторичный критерий: избегать кирпича
            ))

            for new_row, new_col, new_direction in valid_moves:
                cell_value = self.field.level_matrix[new_row][new_col]

                if cell_value == POLE_BASE:
                    # Если перед нами база, стреляем и останавливаемся
                    self.direction = new_direction
                    self.shoot()
                    self.moving = False
                    return

                if self.can_move(new_row, new_col, player_tank):  # Если можно двигаться
                    self.direction = new_direction
                    if cell_value == POLE_KIRPICH and not self.shoot():
                        return

                    # Обновляем позицию и добавляем в список недавних
                    self.target_x, self.target_y = new_col * CELL_SIZE, new_row * CELL_SIZE
                    self.row, self.col = new_row, new_col
                    self.moving = True
                    self.update_recent_positions(row, col)
                    return

        # Если невозможно двигаться, остаемся на месте
        self.moving = False

    def update_recent_positions(self, row, col):
        """Обновляет список недавно посещенных позиций."""
        self.recent_positions.append((row, col))
        if len(self.recent_positions) > 3:  # Храним только последние 3 позиции
            self.recent_positions.pop(0)

    def can_move(self, row, col, player):
        """Проверка, можно ли двигаться на указанную клетку."""
        # Преобразуем row и col в целые числа
        row, col = int(row), int(col)
        if 0 <= row < self.field.rows and 0 <= col < self.field.cols:
            cell_value = self.field.level_matrix[row][col]
            if (row, col) == (player.target_y//CELL_SIZE, player.target_x//CELL_SIZE):
                return False
            if cell_value not in [POLE_BETON, POLE_WATER]:
                return True
        return False

    def move(self):
        """Плавное движение танка к целевой позиции."""
        if self.moving:
            self.x = self.approach(self.x, self.target_x)
            self.y = self.approach(self.y, self.target_y)

            # Проверяем, достиг ли танк целевой позиции
            if self.x == float(self.target_x) and self.y == float(self.target_y):
                self.x = int(self.x)
                self.y = int(self.y)
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
            return False

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
        return True

    def update(self, player_tank):
        """Обновление состояния танка."""
        self.move()
        if not self.moving:
            self.move_towards_base(player_tank)

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

            # Проверка на смерть бота и спавн нового
            if bot.hp <= 0:
                player_tank.score += bot.get_score
                # Убираем мертвого бота
                self.enemies.remove(bot)

                # Случайный выбор новой позиции для спавна и нового типа танка
                spawn_position = random.choice([
                    (row, col) for row in range(self.field.rows)
                    for col in range(self.field.cols)
                    if self.field.level_matrix[row][col] == POLE_VRAGS
                ])
                new_tank_type = random.choice(['ТТ', 'СТ', 'ЛТ'])
                new_bot = TankEnemy(new_tank_type, spawn_position[0], spawn_position[1], self.base_position, self.field)
                self.enemies.append(new_bot)

    def draw(self, screen):
        for bot in self.enemies:
            bot.draw(screen)
