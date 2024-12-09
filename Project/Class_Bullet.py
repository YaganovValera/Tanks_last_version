from CONST import *

SHOT_COOLDOWN = 600         # промежуток между выстрелами


class Bullet:
    def __init__(self, x, y, direction, damage=100, speed=4):
        self.x = x
        self.y = y
        self.image = IMG_BULLET
        self.direction = direction  # Направление ('UP', 'DOWN', 'LEFT', 'RIGHT')
        self.speed = speed  # Скорость пули
        self.damage = damage  # Урон, наносимый пулей
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

    def check_collision(self, field, player, bots):
        """Проверяем столкновение пули с объектами на поле и наносим урон при попадании в игрока или бота."""
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

        # Проверка попадания в игрока или в пулю игрока
        if player is not None:
            if (
                    (self.x // CELL_SIZE, self.y // CELL_SIZE) == (player.x // CELL_SIZE, player.y // CELL_SIZE) or
                    (self.x // CELL_SIZE, self.y // CELL_SIZE) == (player.target_x // CELL_SIZE, player.target_y // CELL_SIZE)
            ):
                player.hp -= self.damage
                self.active = False
            for player_bullet in player.bullets:
                if (self.x // CELL_SIZE, self.y // CELL_SIZE) == (player_bullet.x // CELL_SIZE, player_bullet.y // CELL_SIZE):
                    self.active = False
                    player_bullet.active = False

        # Проверка попадания в ботов или их пулю
        if bots is not None:
            for bot in bots:
                if (
                        (self.x // CELL_SIZE, self.y // CELL_SIZE) == (bot.x // CELL_SIZE, bot.y // CELL_SIZE) or
                        (self.x // CELL_SIZE, self.y // CELL_SIZE) == (bot.target_x // CELL_SIZE, bot.target_y // CELL_SIZE)):
                    bot.hp -= self.damage
                    self.active = False

            for bot in bots:
                for bot_bullet in bot.bullets:
                    if (self.x // CELL_SIZE, self.y // CELL_SIZE) == (bot_bullet.x // CELL_SIZE, bot_bullet.y // CELL_SIZE):
                        self.active = False
                        bot_bullet.active = False

    def update(self, field, player, bots):
        """Обновляет состояние пули."""
        self.move()
        self.check_collision(field, player, bots)

    def draw(self, screen):
        """Отрисовываем пулю."""
        direction_angles = {'UP': 0, 'DOWN': 180, 'LEFT': 90, 'RIGHT': -90}
        rotated_image = pygame.transform.rotate(self.image, direction_angles[self.direction])
        screen.blit(rotated_image, (self.x, self.y))

