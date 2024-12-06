from CONST import *


class Field:
    def __init__(self, level_map):
        """
        Конструктор игрового поля.
        :param level_map: карта для уровня.
        """
        self.level_matrix = level_map
        self.rows = len(level_map)
        self.cols = len(level_map[0])
        self.game_over = False

        # Словарь текстур
        self.textures = {
            POLE_BETON: IMG_POLE_BETON,
            POLE_KIRPICH: IMG_POLE_KIRPICH,
            POLE_BASE: IMG_POLE_BASE,
            POLE_BONUS: IMG_POLE_BONUS,
            POLE_WATER: IMG_POLE_WATER,
            POLE_DBASE: IMG_POLE_DBASE
        }

    def draw(self, screen):
        """
        Отображает поле на экране.
        :param screen: Экран для отрисовки.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.level_matrix[row][col]
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                texture = self.textures.get(cell_value)
                if texture:
                    screen.blit(texture, (x, y))
