from CONST import *

SHOT_COOLDOWN = 600         # промежуток между выстрелами


class Bullet:
    def __init__(self, x, y, direction, speed=4):
        self.x = x
        self.y = y
        self.image = IMG_BULLET
        self.direction = direction  # Направление ('UP', 'DOWN', 'LEFT', 'RIGHT')
        self.speed = speed  # Скорость пули
        self.active = True  # Флаг активности (пуля летит)

    def move(self):
        """Двигаем пулю в заданном направлении."""
        if self.direction == 'UP':
            self.y -= self.speed
        elif self.direction == 'DOWN':
            self.y += self.speed
        elif self.direction == 'LEFT':
            self.x -= self.speed
        elif self.direction == 'RIGHT':
            self.x += self.speed

    def check_collision(self, field):
        """Проверяем столкновение пули с объектами на поле."""
        cell_x = self.x // CELL_SIZE
        cell_y = self.y // CELL_SIZE

        if not (0 <= cell_x < field.cols and 0 <= cell_y < field.rows):
            self.active = False  # Пуля вышла за пределы карты
            return

        cell_value = field.level_matrix[cell_y][cell_x]

        # Уничтожение кирпичных блоков
        if cell_value == POLE_KIRPICH:
            field.level_matrix[cell_y][cell_x] = POLE_EMPTY
            self.active = False

        # Уничтожение базы
        if cell_value == POLE_BASE:
            field.level_matrix[cell_y][cell_x] = POLE_DBASE
            field.game_over = True  # Устанавливаем флаг окончания игры
            self.active = False

        # Проверка столкновения с бетоном (не разрушается)
        if cell_value == POLE_BETON:
            self.active = False

    def update(self, field):
        """Обновляет состояние пули."""
        self.move()
        self.check_collision(field)

    def draw(self, screen):
        """Отрисовываем пулю."""
        direction_angles = {'UP': 0, 'DOWN': 180, 'LEFT': 90, 'RIGHT': -90}
        rotated_image = pygame.transform.rotate(self.image, direction_angles[self.direction])
        screen.blit(rotated_image, (self.x, self.y))