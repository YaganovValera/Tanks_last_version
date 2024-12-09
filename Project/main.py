import sys
import GameManager
import CONST
import pygame

# Опции меню
MENU_OPTIONS = ["Новая игра", "Номер уровня: ", "Выход"]
OPTION_NEW_GAME = 0
OPTION_LEVEL = 1
OPTION_EXIST = 2

# Количество уровней
MAX_LVL = 3
MIN_LVL = 1

selected_option = OPTION_NEW_GAME                               # Индекс выбранного пункта
level_number = 1                                                # Начальный уровень


def draw_menu(screen, font):
    global selected_option
    global level_number
    """Функция для отрисовки меню."""
    screen.fill(CONST.WHITE)  # Очистка экрана
    title = font.render("Меню", True, CONST.BLACK)
    screen.blit(title, (CONST.WIDTH // 2 - title.get_width() // 2, 50))  # Заголовок

    for i, option in enumerate(MENU_OPTIONS):
        # Если это пункт "Номер уровня", добавляем текущее значение уровня
        text_content = option + str(level_number) if "Номер уровня" in option else option
        color = CONST.GREEN if i == selected_option else CONST.BLACK
        text = font.render(text_content, True, color)
        screen.blit(text, (CONST.WIDTH // 2 - text.get_width() // 2, 150 + i * 60))


def run_game():
    try:
        global selected_option
        global level_number

        # Инициализация pygame
        pygame.init()

        # Настройки окна
        screen = pygame.display.set_mode((CONST.WIDTH, CONST.HEIGHT))
        pygame.display.set_caption("Танчики: Меню")

        # Шрифт
        font = pygame.font.Font(None, 50)

        # Главный цикл меню
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Обработка нажатий клавиш
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(MENU_OPTIONS)  # Перемещение вверх
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(MENU_OPTIONS)  # Перемещение вниз
                    elif event.key == pygame.K_RETURN:
                        if selected_option == OPTION_NEW_GAME:
                            try:
                                game = GameManager.GameManager(level_number)
                                game.run()
                            except Exception as e:
                                print(f"Ошибка при запуске игры: {e}")
                        elif selected_option == OPTION_EXIST:
                            running = False
                    if selected_option == OPTION_LEVEL:
                        if event.key == pygame.K_LEFT:
                            level_number = max(MIN_LVL, level_number - 1)  # Минимальный уровень
                        elif event.key == pygame.K_RIGHT:
                            level_number = min(MAX_LVL, level_number + 1)  # Максимальный уровень

            draw_menu(screen, font)
            pygame.display.flip()
            clock.tick(30)
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    run_game()
