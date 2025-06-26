import copy

class SudokuSolver:
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.solution = None
        self.steps = []
        self.current_step = 0
        self.solved = False
        self.find_solution()  # Находим полное решение сразу

    def find_solution(self):
        """Находит полное решение и сохраняет все шаги"""
        temp_board = copy.deepcopy(self.board)
        self._solve_with_backtracking(temp_board)
        if self.solution:
            self._record_steps()

    def _solve_with_backtracking(self, board):
        """Рекурсивный backtracking-алгоритм"""
        empty = self.find_empty(board)
        if not empty:
            self.solution = copy.deepcopy(board)
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num

                if self._solve_with_backtracking(board):
                    return True

                board[row][col] = 0
        return False

    def get_next_step(self):
        """Возвращает следующий шаг решения"""
        if not self.solution or self.current_step >= len(self.steps):
            return None

        step = self.steps[self.current_step]
        self.current_step += 1
        return step

    def _record_steps(self):
        """Записывает все шаги решения"""
        temp_board = copy.deepcopy(self.board)
        self.steps = []

        def solve_and_record(board):
            empty = self.find_empty(board)
            if not empty:
                return True

            row, col = empty
            for num in range(1, 10):
                if self.is_valid(board, num, (row, col)):
                    board[row][col] = num
                    self.steps.append((row, col, num))  # Записываем шаг

                    if solve_and_record(board):
                        return True

                    board[row][col] = 0
                    self.steps.append((row, col, 0))  # Откат шага
            return False

        solve_and_record(temp_board)

    @staticmethod
    def find_empty(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    @staticmethod
    def is_valid(board, num, pos):
        # Проверка строки
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Проверка столбца
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Проверка квадрата 3x3
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True