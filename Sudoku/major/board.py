import pygame
import random
import copy
from major.constants import GRID_SIZE

class SudokuBoard:
    def __init__(self, difficulty="None"):
        self.difficulty = difficulty
        self.board = [[0 for _ in range(9)] for _ in range(9)]  # Добавил
        solve(self.board)
        remove_numbers(self.board, self.difficulty)
        self.original = copy.deepcopy(self.board)  # Сохраняем исходное состояние
        self.emptied_board = [[0 for _ in range(9)] for _ in range(9)]

    def generate_board(self, difficulty):
        """Генерирует новое поле судоку."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        solve(board)  # Сначала решаем, чтобы получить валидную доску
        remove_numbers(board, difficulty)  # Потом удаляем числа
        return board

    def clear(self):
        self.board = copy.deepcopy(self.emptied_board)
        self.original = copy.deepcopy(self.emptied_board)  # Обновляем original

    def get_cell(self, row, col):
        return self.board[row][col] if 0 <= row < 9 and 0 <= col < 9 else None

    def set_cell(self, row, col, value, is_original=False):
        """Устанавливает значение клетки с проверкой допустимости"""
        if not (0 <= row < 9 and 0 <= col < 9):
            return False

        if not (0 <= value <= 9):
            return False

        self.board[row][col] = value
        return True

def is_valid(board, row, col, num):
    """Проверяет, допустимо ли число num в позиции (row, col) доски."""
    # Проверка строки
    if num in board[row]:
        return False

    # Проверка столбца
    if num in [board[i][col] for i in range(9)]:
        return False

    # Проверка блока 3x3
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve(board):
    """Решает судоку с помощью алгоритма backtracking."""
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    nums = list(range(1, 10))
    random.shuffle(nums)  # Перемешиваем числа для случайности

    for i in nums:
        if is_valid(board, row, col, i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0  # Откат
    return False

def find_empty(board):
    """Находит пустую клетку (со значением 0) в доске."""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None

def has_unique_solution(board):
    """Проверяет, имеет ли судоку единственное решение."""
    temp_board = copy.deepcopy(board)
    solve(temp_board)
    if find_empty(temp_board) is not None:  # Есть несколько решений
        return False

    return True

def remove_numbers(board, difficulty):
    """Удаляет числа из решенной доски в зависимости от сложности."""
    if difficulty == "Easy":
        num_to_remove = 25
    elif difficulty == "Medium":
        num_to_remove = 40
    elif difficulty == "Hard":
        num_to_remove = 50
    else:
        num_to_remove = 40  # Значение по умолчанию

    removed_count = 0
    attempts = 500

    while removed_count < num_to_remove and attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if board[row][col] != 0:
            temp_value = board[row][col]
            board[row][col] = 0

            copy_board = copy.deepcopy(board)  # Копируем доску перед проверкой
            if not solve(copy_board):
                board[row][col] = temp_value  # Возвращаем число обратно, если нет решения
            else:
                board_copy = copy.deepcopy(board)
                solutions = []
                solve_for_all_solutions(board_copy, solutions)

                if len(solutions) != 1:
                    board[row][col] = temp_value
                else:
                    removed_count += 1

        attempts -= 1

    print(f"Removed {removed_count} numbers for difficulty {difficulty}")

def solve_for_all_solutions(board, solutions):
    """Решает судоку и находит все возможные решения."""
    empty_cell = find_empty(board)
    if not empty_cell:
        # Доска решена, сохраняем решение
        solution = [row[:] for row in board]
        solutions.append(solution)
        return

    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            solve_for_all_solutions(board, solutions)
            board[row][col] = 0  # Сбрасываем значение при возврате