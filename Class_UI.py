from CONST import *

# Константы панели
PANEL_WIDTH = WIDTH - HEIGHT      # Ширина панели
PANEL_HEIGHT = HEIGHT             # Высота панели
PANEL_X = HEIGHT                  # Начальная координата X панели
PANEL_Y = 0                       # Начальная координата Y панели


class InfoPanel:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 30)  # Шрифт для текста

    def draw(self):
        """Отрисовывает панель информации."""
        # Задний фон панели
        panel_rect = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect)

        # Текстовая информация
        info_texts = [
            f"Уровень: {int(self.player.lvl)}",
            f"Счет: {int(self.player.score)}",
            f"Жизней: {int(self.player.live)}",
            f"HP танка: {int(self.player.hp)}",
        ]

        # Отрисовка текста
        for i, text in enumerate(info_texts):
            text_surface = self.font.render(text, True, WHITE)  # Белый текст
            self.screen.blit(text_surface, (PANEL_X + 10, 10 + i * 30))  # Положение текста на панели
