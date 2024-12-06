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
            (field=self.field, position=start_position(lev[level_number - 1], CONST.POLE_PLAYER))
        self.info_panel = Class_UI.InfoPanel(self.screen, self.player_tank)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            # self.check_game_over()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player_tank.handle_keys(event)             # Обработка ввода игрока

    def update(self):
        self.bonus.update()
        self.enemy_tanks.update()
        self.player_tank.update()  # Обновление игрока

    def render(self):
        self.screen.fill(CONST.BLACK)
        self.field.draw(self.screen)
        self.enemy_tanks.draw(self.screen)
        self.player_tank.draw(self.screen)
        self.info_panel.draw()
        pygame.display.flip()

    def check_game_over(self):
        # Логика завершения игры (например, смерть игрока или уничтожение базы)
        if self.field.game_over:
            self.end_game("База разрушена! Игра окончена.")
        elif self.player_tank.dead > CONST.MAX_DEAD:
            self.end_game("Слишком много смертей! Игра окончена.")

    def end_game(self, message):
        print(message)
        self.running = False
