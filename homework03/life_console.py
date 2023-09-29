import curses
import msvcrt

from life import GameOfLife
from ui import UI
import time

class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addch(0, 0, '+')
        screen.addch(0, self.life.cols + 1, '+')
        screen.addch(self.life.rows + 1, 0, '+')
        screen.addch(self.life.rows + 1, self.life.cols + 1, '+')

        for row in range(1, self.life.rows + 1):
            screen.addch(row, 0, '|')
            screen.addch(row, self.life.cols + 1, '|')

        for col in range(1, self.life.cols + 1):
            screen.addch(0, col, '-')
            screen.addch(self.life.rows + 1, col, '-')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[col][row]:
                    screen.addch(row + 1, col + 1, '*')
                else:
                    screen.addch(row + 1, col + 1, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        
        pause = False
        sleep_time = 0.6
        curses.noecho()
        while self.life.is_changing and not self.life.is_max_generations_exceeded:

            if msvcrt.kbhit() and chr(screen.getch()) == 'q':
                break
            if msvcrt.kbhit() and chr(screen.getch()) == 'p':
                pause = not pause
            if pause == True:
                continue

            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(sleep_time)
            self.life.step()

        curses.endwin()


life = GameOfLife(size=(20, 40), randomize=True)
console_ui = Console(life)
console_ui.run()