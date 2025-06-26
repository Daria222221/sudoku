import pygame
from major.board import is_valid

class BoardChecker:
    def __init__(self, board, font):
        self.board = board
        self.font = font
        self.errors = []  # Список координат (row, col) с ошибками
        self.show_errors = False  # Показывать ошибки или нет
        self.error_duration = 3000  # 3 секунды
        self.error_start_time = 0

    def reset(self, board):
        self.board = board
        self.errors = []
        self.show_errors = False
        self.error_start_time = 0

    def check_board(self):
        """Проверяет доску на наличие ошибок и возвращает True, если все в порядке."""
        print("check_board called")
        self.errors = []  # Очищаем список ошибок
        has_empty_cells = False
        for i in range(9):
            for j in range(9):
                num = self.board.board[i][j]
                if num == 0:
                    has_empty_cells = True
                elif not is_valid(self.board.board, i, j, num):
                    self.errors.append((i, j))

        if self.errors:
            self.show_errors = True
            self.error_start_time = pygame.time.get_ticks()
            print("Errors found:", self.errors)  # Печатаем найденные ошибки
            return False  # Есть ошибки

        if has_empty_cells:
            self.show_errors = False
            print("Incomplete board")
            return "incomplete"  # Доска заполнена не полностью

        self.show_errors = False
        print("Board is solved!")
        return True  # Доска решена

    def draw_errors(self, screen, cell_size, grid_pos):
        """Подсвечивает клетки с ошибками красным цветом."""
        if self.show_errors:
            current_time = pygame.time.get_ticks()
            if current_time - self.error_start_time < self.error_duration:
                for row, col in self.errors:
                    x = grid_pos[0] + col * cell_size
                    y = grid_pos[1] + row * cell_size
                    rect = pygame.Rect(x, y, cell_size, cell_size)
                    pygame.draw.rect(screen, (255, 0, 0), rect, 3)  # Красная рамка
            else:
                self.show_errors = False  # Скрываем подсветку после 3 секунд