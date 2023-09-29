import random
import typing as tp

import pygame
from pygame.locals import *
from copy import deepcopy

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.Grid = self.create_grid(True)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            
            self.screen.fill(pygame.Color("white"))

            self.draw_grid()
            self.grid = self.get_next_generation()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """ 
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        Grid = [[0 for _ in range(int(self.width/self.cell_size))] for _ in range(int(self.height/self.cell_size))]

        if randomize:
        # Генерируем случайные значения 0 или 1 для каждой клетки в матрице
            for i in range(int(self.width/self.cell_size)):
                for j in range(int(self.height/self.cell_size)):
                    Grid[j][i] = random.randint(0,1)
        else:
            # Создаем матрицу из нулей (все клетки мертвы)
            for i in range(int(self.width/self.cell_size)):
                for j in range(int(self.height/self.cell_size)):
                    Grid[j][i] = 0
        self.grid = Grid
        # Возвращаем созданную матрицу клеток
        return Grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        # Цвета для живых и мертвых клеток
        alive_color = pygame.Color('green')
        dead_color = pygame.Color('white')

        # Размер клетки (прямоугольника)
        cell_size = self.cell_size

        # Проходим по всем клеткам в матрице
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                # Получаем значение клетки (1 - живая, 0 - мертвая)
                cell_value = self.grid[row][col]

                # Вычисляем координаты прямоугольника для текущей клетки
                x = col * cell_size
                y = row * cell_size

                # Создаем прямоугольник
                cell_rect = pygame.Rect(x, y, cell_size, cell_size)

                # Отрисовываем прямоугольник и закрашиваем его в соответствующий цвет
                if cell_value == 1:
                    pygame.draw.rect(self.screen, alive_color, cell_rect)
                else:
                    pygame.draw.rect(self.screen, dead_color, cell_rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """

        neighbors = []
        row, col = cell  # Разделим координаты клетки на строку и столбец

        # Перебираем соседние клетки вокруг данной клетки
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Исключаем клетку саму себя
                if dr == 0 and dc == 0:
                    continue

                # Вычисляем координаты соседней клетки
                neighbor_row = row + dr
                neighbor_col = col + dc

                # Проверяем, что соседние координаты находятся в пределах матрицы Grid
                if 0 <= neighbor_row < len(self.grid) and 0 <= neighbor_col < len(self.grid[0]):
                    # Добавляем соседнюю клетку в список соседей
                    neighbors.append(self.grid[neighbor_row][neighbor_col])

        return neighbors

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        new_grid = deepcopy(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                a = sum(self.get_neighbours((i, j)))
                if self.grid[i][j]:
                    if a in (2, 3):
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if a == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid
        return self.grid

g = GameOfLife()
g.run()
