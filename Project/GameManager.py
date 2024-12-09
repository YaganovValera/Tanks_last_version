import copy
import time

import CONST
import pygame
from Levels import lev
import Class_Field
import Class_Bonus
import Class_EnemyTank
import Class_PlayerTank
import Class_UI


class GameManager:
    def __init__(self, level_number):
        pygame.init()
        map_lvl = copy.deepcopy(lev[level_number - 1])
        self.screen = pygame.display.set_mode((CONST.WIDTH, CONST.HEIGHT))
        pygame.display.set_caption("Танчики")
        self.clock = pygame.time.Clock()
        self.running = True

        # Инициализация компонентов игры
        self.field = Class_Field.Field(map_lvl)
        self.bonus = Class_Bonus.Bonus(field=self.field)
        self.enemy_tanks = Class_EnemyTank.BotManager(field=self.field)
        self.player_tank = Class_PlayerTank.Player(field=self.field)
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
            self.player_tank.handle_keys(event, self.enemy_tanks.enemies)             # Обработка ввода игрока

    def update(self):
        self.player_tank.update(self.bonus, None, self.enemy_tanks.enemies)  # Обновление игрока
        self.enemy_tanks.update(self.player_tank)
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
        elif self.player_tank.live == self.player_tank.get_MIN_live():
            self.end_game("Вы потратили все жизни! Игра окончена.")
        elif self.player_tank.score >= self.player_tank.get_MAX_score():
            self.end_game("Победа!")

    def end_game(self, message):
        font = pygame.font.Font(None, 50)
        text_surface = font.render(message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(CONST.WIDTH // 2, CONST.HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        self.running = False
        start_time = pygame.time.get_ticks()

        # Основной цикл, который будет работать до тех пор, пока не пройдет 5 секунд
        while True:
            current_time = pygame.time.get_ticks()

            # Проверяем, прошло ли 5 секунд
            if current_time - start_time >= 5000:
                return
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                    return
