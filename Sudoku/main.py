import pygame
import sys
import os  # Для работы с путями
import pickle  # Для сохранения данных в файл
import random

from major.board import SudokuBoard
from Solver.solver import SudokuSolver
from interface.buttons import Button
from interface.grid import draw_grid, draw_numbers, get_clicked_cell
from interface.theme import draw_gradient
from major.constants import *
from Save_and_Load.load_game_menu import LoadGameMenu
from Save_and_Load.save_game_menu import SaveGameMenu
from Save_and_Load.autosave import autosave_game  # Импортируем функцию autosave_game
from interface.PopupMenu import PopupMenu  # Import PopupMenu
from major.exit import ExitButton
from major.win import WinAnimation  # Импортируем WinAnimation
from major.board_checker import BoardChecker


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("SudokuSolver")
    font = pygame.font.SysFont(None, 32)
    title_font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    global board, selected_cell, win_animation, solving, solving_step_delay, last_step_time, board_checker
    solving = False
    solving_step_delay = 100
    last_step_time = 0

    board = SudokuBoard()
    selected_cell = None
    exit_button = ExitButton(WIDTH - 55, 25, 20, DARK_BLUE, RED)
    board_checker = BoardChecker(board, font)  # Эта строка должна быть ДО вызовов new_game()
    win_animation = None

    # Создаем корневую папку проекта
    root_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(root_dir, "save_game")

    # Создаем папку save_game, если ее нет
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Определяем функцию для новой игры с выбором сложности
    def new_game(difficulty="Medium"):
        global board, selected_cell, win_animation, board_checker
        board = SudokuBoard(difficulty)  # Создаем новую доску
        selected_cell = None
        win_animation = None
        board_checker.reset(board)

    # Функция для показа меню выбора сложности
    def show_difficulty_menu():
        difficulty_menu.visible = True

    def save_game():
        global save_menu
        save_menu = SaveGameMenu(screen, root_dir, save_game_to_file, close_save_menu)

    def save_game_to_file(file_name):
        global last_saved_filename
        last_saved_filename = file_name
        file_path = os.path.join(save_dir, file_name + ".sudoku")

        try:
            with open(file_path, "wb") as f:
                data = {
                    "board": board.board,
                    "original": board.original,
                    "difficulty": board.difficulty,
                }
                pickle.dump(data, f)
            print(f"Game saved to {file_path}")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game():
        global load_menu
        load_menu = LoadGameMenu(screen, root_dir, load_data_into_game, close_load_menu)

    def load_data_into_game(data):
        global board
        board.board = data["board"]
        board.original = data["original"]
        board.difficulty = data["difficulty"]

    def close_load_menu():
      global load_menu
      load_menu = None

    def close_save_menu():
        global save_menu
        save_menu = None

        # Создаем всплывающее меню

    button_x = (WIDTH - 160) // 2
    button_y = GRID_POS[1] + GRID_SIZE + 25
    menu_x = button_x - 20  # Центрируем меню относительно кнопки
    menu_y = button_y - 160  # Ставим меню над кнопкой (высота кнопки + небольшой отступ)
    menu_width = 200
    menu_height = 150  # Достаточно места для 3 опций
    menu_options = ["Easy", "Medium", "Hard"]
    difficulty_menu = PopupMenu(menu_x, menu_y, menu_width, menu_height, menu_options)
    difficulty_menu.visible = False

    # Инициализация кнопок
    buttons = [
        Button(WIDTH - 180, 100, 160, 50, "Создать",
               lambda: board.clear()),
        Button(WIDTH - 180, 180, 160, 50, "Решить", lambda: handle_solve_button()),
        Button(WIDTH - 180, 250, 160, 50, "Проверить",
               lambda: handle_check_button()),
        Button(WIDTH - 180, 320, 160, 50, "Save",
               lambda: save_game()),
        Button(WIDTH - 180, 390, 160, 50, "Autosave",  # ИЗМЕНЕНО
               lambda: save_game_second()),#ИЗМЕНЕНО
        Button(WIDTH - 180, 460, 160, 50, "Загрузить",
               lambda: load_game()),
        Button((WIDTH - 160) // 2, GRID_POS[1] + GRID_SIZE + 25, 160, 50, "Новая игра",
               lambda: show_difficulty_menu()),
    ]

    def save_game_second(): # Добавляем autosave_game в main
      global last_saved_filename
      board_data = {"board": board.board,
                    "original": board.original,
                    "difficulty": board.difficulty}

      last_saved_filename = autosave_game(save_dir, board_data, last_saved_filename)

    global load_menu
    load_menu = None

    global save_menu
    save_menu = None

    def handle_check_button():
        global win_animation
        print("handle_check_button called")
        print("Board object ID:", id(board.board))  # Добавим это
        print("Current board state:")
        for row in board.board:
            print(row)
        result = board_checker.check_board()
        print("check_board result:", result)
        if result == True:
            print("Доска решена! Запускаем анимацию победы!")
            # Запускаем анимацию победы
            win_animation = WinAnimation(screen, board.board, font, GRID_POS, CELL_SIZE)
        elif result == "incomplete":
            print("Доска заполнена не полностью")
            # Выводим сообщение на 3 секунды
        else:
            print("На доске есть ошибки! Подсвечиваем их красным.")
            # Подсвечиваем ошибки
            win_animation = None  # Гасим анимацию при наличии ошибок

    def handle_solve_button():
        """Вставляет одно правильное число из заранее вычисленного решения"""
        # Находим первую пустую клетку
        for row in range(9):
            for col in range(9):
                if board.board[row][col] == 0:  # Если клетка пустая
                    # Берем значение из решения
                    correct_num = board.solution[row][col]
                    board.board[row][col] = correct_num

                    # Подсвечиваем добавленное число
                    global selected_cell
                    selected_cell = (row, col)

                    # Проверяем, не завершена ли игра
                    handle_check_button()
                    return  # Выходим после добавления одного числа

        # Если пустых клеток нет
        print("Все клетки уже заполнены!")

    global last_saved_filename
    last_saved_filename = None

    while True:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if solving and current_time - last_step_time > solving_step_delay:
                changed_cell = SudokuSolver.solve_step(board.board)
                last_step_time = current_time

                if changed_cell:
                    selected_cell = changed_cell  # Подсветим изменённую клетку
                else:
                    solving = False  # Решение завершено
                    handle_check_button()  # Проверим решение

            # Обработка событий для кнопки выхода
            if exit_button.handle_event(event):
                pygame.quit()
                sys.exit()

            difficulty_menu.handle_event(event)  # Обрабатываем события меню

            if difficulty_menu.selected_option:
                new_game(difficulty_menu.selected_option)
                difficulty_menu.selected_option = None

            if save_menu:
              save_menu.handle_event(event)
              continue

            # Если открыто окно загрузки, передаем ему события
            if load_menu:
                load_menu.handle_event(event)
                continue

            # Обработка клика по крестику
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if mouse_on_exit(mouse_pos):
                #     pygame.quit()
                #     sys.exit()

                # Обработка клика по сетке
                cell = get_clicked_cell(mouse_pos)
                if cell:
                    selected_cell = cell
                else:
                    selected_cell = None

            # Обработка ввода с клавиатуры
            elif event.type == pygame.KEYDOWN and selected_cell:
                row, col = selected_cell
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.set_cell(row, col, 0)  # Очистить клетку
                elif event.unicode.isdigit() and event.unicode != '0':
                    board.set_cell(row, col, int(event.unicode))  # Ввести цифру

            # Обработка кнопок
            for btn in buttons:
                btn.handle_event(event)




        # Отрисовка
        draw_gradient(screen, (100, 140, 210), (200, 230, 255))

        # Заголовок
        title = title_font.render("SudokuSolver", True, DARK_BLUE2)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))

        # Сетка и числа
        draw_grid(screen, *GRID_POS, GRID_SIZE, mouse_pos)
        draw_numbers(screen, board, *GRID_POS, GRID_SIZE, font)

        # Подсветка выбранной клетки
        if selected_cell:
            row, col = selected_cell
            highlight_x = GRID_POS[0] + col * CELL_SIZE
            highlight_y = GRID_POS[1] + row * CELL_SIZE
            pygame.draw.rect(screen, (0, 50, 200),
                                 (highlight_x, highlight_y, CELL_SIZE, CELL_SIZE), 3)

        # Кнопки
        for btn in buttons:
            btn.draw(screen)

        difficulty_menu.draw(screen, font)  # Отрисовываем меню

        if load_menu:
            load_menu.draw(screen)

        if save_menu:
            save_menu.draw(screen)

        if win_animation:
            animation_finished = win_animation.draw()
            if animation_finished:
                win_animation = None  # Завершаем анимацию
        board_checker.draw_errors(screen, CELL_SIZE, GRID_POS)

        # Рисуем кнопку выхода
        exit_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)





def solve():  # Передаем self
    SudokuSolver.solve(board.board)

if __name__ == "__main__":
    main()