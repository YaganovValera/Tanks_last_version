from CONST import *
import Class_Bullet

MAX_LVL_PLAYER = 3
MIN_LVL_PLAYER = 1

MAX_SCORE_PLAYER = 0
MIN_SCORE_PLAYER = 0

MAX_HP = 100
MIN_HP = 0

MIN_DEAD = 0
MAX_DEAD = 10


class Player:
    def __init__(self, field, position, speed=2):
        self.lvl = MIN_LVL_PLAYER
        self.score = MIN_SCORE_PLAYER
        self.dead = MIN_DEAD
        self.hp = MAX_HP
        y, x = position
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.image = IMG_POLE_PLAYER
        self.direction = 'UP'
        self.target_x = self.x
        self.target_y = self.y
        self.moving = False
        self.movement_key = None

        self.speed = speed
        self.field = field
        self.bullets = []
        self.last_shot_time = 0
        self.shot_cooldown = Class_Bullet.SHOT_COOLDOWN

    def shoot(self):
        """Стрельба игрока."""
        directions = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0),
        }

        if self.direction in directions:
            dx, dy = directions[self.direction]

            for i in range(self.lvl):  # Количество пуль = уровень игрока
                offset = i * 10  # Смещение пуль (например, по 10 пикселей)
                # Вычисляем начальную позицию пули
                bullet_x = self.x + offset * dx
                bullet_y = self.y + offset * dy
                # Создаём новый снаряд и добавляем его в список
                bullet = Class_Bullet.Bullet(bullet_x, bullet_y, self.direction)
                self.bullets.append(bullet)
        # Обновляем время последнего выстрела
        self.last_shot_time = pygame.time.get_ticks()

    def can_shoot(self):
        """Проверяет, можно ли стрелять (учитывает задержку)."""
        return pygame.time.get_ticks() - self.last_shot_time >= self.shot_cooldown

    def handle_keys(self, event):
        """Обрабатываем нажатия и отпускания клавиш."""
        directions = {
            pygame.K_UP: ('UP', 0, -1),
            pygame.K_DOWN: ('DOWN', 0, 1),
            pygame.K_LEFT: ('LEFT', -1, 0),
            pygame.K_RIGHT: ('RIGHT', 1, 0),
        }

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.can_shoot():
                self.shoot()  # Вызываем стрельбу, движение не блокируется

            if not self.moving and event.key in directions:
                self.direction, dx, dy = directions[event.key]
                if self.can_move_to(dx, dy):
                    self.target_x += dx * CELL_SIZE
                    self.target_y += dy * CELL_SIZE
                    self.movement_key = event.key
                    self.moving = True

        elif event.type == pygame.KEYUP and event.key == self.movement_key:
            self.movement_key = None

    def can_move_to(self, dx, dy):
        """Проверяем, можно ли двигаться на клетку."""
        cell_x = (self.x // CELL_SIZE) + dx
        cell_y = (self.y // CELL_SIZE) + dy

        if not (0 <= cell_x < self.field.cols and 0 <= cell_y < self.field.rows):
            return False

        return self.field.level_matrix[cell_y][cell_x] in [POLE_EMPTY, POLE_PLAYER, POLE_VRAGS]

    def move(self):
        """Плавное движение игрока к целевой позиции."""
        if self.moving:
            self.x = self.approach(self.x, self.target_x)
            self.y = self.approach(self.y, self.target_y)

            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False
                if self.movement_key:
                    self.handle_keys(pygame.event.Event(pygame.KEYDOWN, key=self.movement_key))

    def approach(self, current, target):
        """Помогает двигаться к целевой координате с учетом скорости."""
        if current < target:
            return min(current + self.speed, target)
        elif current > target:
            return max(current - self.speed, target)
        return current

    def update(self):
        """Обновляет состояние игрока и его пуль."""
        self.move()
        for bullet in self.bullets[:]:
            bullet.update(self.field)
            if not bullet.active:
                self.bullets.remove(bullet)

    def draw(self, screen):
        """Отрисовка игрока с поворотом."""
        direction_angles = {'UP': 0, 'DOWN': 180, 'LEFT': 90, 'RIGHT': -90}
        rotated_image = pygame.transform.rotate(self.image, direction_angles[self.direction])
        screen.blit(rotated_image, (self.x, self.y))

        # Отрисовываем снаряды
        for bullet in self.bullets:
            bullet.draw(screen)
