import pathlib
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
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        Grid = [[0 for _ in range(int(self.rows))] for _ in range(int(self.cols))]

        if randomize:
        # Генерируем случайные значения 0 или 1 для каждой клетки в матрице
            for j in range(int(self.cols)):
                for i in range(int(self.rows)):
                    Grid[j][i] = random.randint(0,1)
        else:
            # Создаем матрицу из нулей (все клетки мертвы)
            for j in range(int(self.cols)):
                for i in range(int(self.rows)):
                    Grid[j][i] = 0
        self.grid = Grid
        # Возвращаем созданную матрицу клеток
        return self.grid

    def get_neighbours(self, cell: Cell) -> Cells:
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

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as file:
        # Read the lines from the file and parse them to create the grid
            lines = file.readlines()
            grid = [[int(cell) for cell in line.strip()] for line in lines]

            # Размеры сетки
            rows = len(grid)
            cols = len(grid[0])

            game = GameOfLife(size=(rows, cols), randomize=False)
            game.curr_generation = grid
            return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as file:
            for row in self.curr_generation:
                # Convert each row of the grid to a string and write it to the file
                row_str = "".join(str(cell) for cell in row)
                file.write(row_str + "\n")

