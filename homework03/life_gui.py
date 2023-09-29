import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed 
        self.screen_size = life.cols * self.cell_size, life.rows * self.cell_size
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        width, height = self.screen_size
        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (width, y))

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
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                # Получаем значение клетки (1 - живая, 0 - мертвая)
                cell_value = self.life.grid[row][col]

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

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.Grid = life.create_grid(True)
        
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONDOWN and pause:
                    x, y = pygame.mouse.get_pos()
                    row = y // self.cell_size
                    col = x // self.cell_size
                    self.life.grid[row][col] = (self.life.grid[row][col] + 1) % 2
            
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()

            if pause:
                continue

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            
            self.grid = life.get_next_generation()
            clock.tick(self.speed)

        pygame.quit()

life = GameOfLife((25, 25))
g = GUI(life)
g.run()