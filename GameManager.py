import CONST
import pygame
from Levels import lev
import Class_Field
import Class_Bonus
import Class_EnemyTank
import Class_PlayerTank
import Class_UI


def start_position(matrix, POLE):
    """Находит стартовую позицию игрока на поле."""
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if matrix[row][column] == POLE:
                return (row, column)


class GameManager:
    def __init__(self, level_number):
        pygame.init()
        self.screen = pygame.display.set_mode((CONST.WIDTH, CONST.HEIGHT))
        pygame.display.set_caption("Танчики")
        self.clock = pygame.time.Clock()
        self.running = True

        # Инициализация компонентов игры
        self.field = Class_Field.Field(lev[level_number - 1])
        self.bonus = Class_Bonus.Bonus(field=self.field)
        self.enemy_tanks = Class_EnemyTank.BotManager(field=self.field)
        self.player_tank = Class_PlayerTank.Player\
            (field=self.field, position=start_position(lev[level_number - 1], CONST.POLE_PLAYER), bonus=self.bonus)
        self.info_panel = Class_UI.InfoPanel(self.screen, self.player_tank)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.check_game_over()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player_tank.handle_keys(event)             # Обработка ввода игрока

    def update(self):
        self.enemy_tanks.update()
        self.player_tank.update()  # Обновление игрока
        self.bonus.update()

    def render(self):
        self.screen.fill(CONST.BLACK)
        self.field.draw(self.screen)
        self.enemy_tanks.draw(self.screen)
        self.player_tank.draw(self.screen)
        self.info_panel.draw()
        pygame.display.flip()

    def check_game_over(self):
        # Логика завершения игры
        if self.field.game_over:
            self.end_game("База разрушена! Игра окончена.")
        elif self.player_tank.live == 0:
            self.end_game("Вы потратили все жизни! Игра окончена.")

    def end_game(self, message):
        font = pygame.font.Font(None, 50)
        text_surface = font.render(message, True, (78, 255, 33))
        text_rect = text_surface.get_rect(center=(CONST.WIDTH // 2, CONST.HEIGHT // 2))

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        self.running = False

        start_time = pygame.time.get_ticks()

        # Основной цикл, который будет работать до тех пор, пока не пройдет 5 секунд
        while True:
            current_time = pygame.time.get_ticks()

            # Проверяем, прошло ли 5 секунд
            if current_time - start_time >= 15000:
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                    return

            pygame.time.Clock().tick(30)

