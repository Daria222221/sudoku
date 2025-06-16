import pygame
import os
import pickle
from major.constants import *
from Save_and_Load.utils import get_saved_games, create_button
from interface.theme import draw_gradient  # !!! ДОБАВЬ ЭТУ СТРОКУ !!!

class LoadGameMenu:
    def __init__(self, screen, root_dir, load_callback, close_callback):
        self.screen = screen
        self.root_dir = root_dir
        self.save_dir = os.path.join(self.root_dir, "save_game")  # Путь к папке сохранений
        self.load_callback = load_callback  # Функция для загрузки данных в игру
        self.close_callback = close_callback  # Функция закрытия меню загрузки
        self.font = pygame.font.SysFont(None, 32)  # Шрифт для текста
        self.running = True
        self.selected_file = None  # Выбранный файл сохранения
        self.file_list = get_saved_games(self.save_dir)  # Получаем список файлов
        self.file_buttons = []  # Кнопки для файлов

        # Определяем позиции кнопок
        button_width = 150
        button_height = 50
        button_y = 450  # Фиксированная позиция по Y
        total_button_width = button_width * 3  # Три кнопки
        spacing = 20 # Расстояние между кнопками
        total_spacing = spacing * 2 # Всего расстояния между кнопками

        # Вычисляем начальную позицию X для центрирования
        start_x = (WIDTH - total_button_width - total_spacing) // 2

        self.load_button_rect = pygame.Rect(start_x, button_y, button_width, button_height)
        self.delete_button_rect = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
        self.close_button_rect = pygame.Rect(start_x + 2 * (button_width + spacing), button_y, button_width, button_height)


        # Создаем кнопки для каждого файла
        self.create_file_buttons()

    def create_file_buttons(self):
        """Создает кнопки для каждого файла сохранения."""
        self.file_buttons = []
        y_offset = 50
        for i, file in enumerate(self.file_list):
            button_rect = pygame.Rect((WIDTH - 500) // 2, y_offset + i * 40, 500, 30) # Center
            self.file_buttons.append((button_rect, file))

    def handle_event(self, event):
        """Обрабатывает события окна загрузки."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Обработка выбора файла
            for button_rect, file in self.file_buttons:
                if button_rect.collidepoint(mouse_pos):
                    self.selected_file = file
                    break  # Выходим из цикла после выбора файла

            # Кнопка загрузки
            if self.load_button_rect.collidepoint(mouse_pos) and self.selected_file:
                self.load_selected_game()

            # Кнопка удаления
            if self.delete_button_rect.collidepoint(mouse_pos) and self.selected_file:
                self.delete_selected_game()

            # Кнопка закрытия
            if self.close_button_rect.collidepoint(mouse_pos):
                self.running = False
                self.close_callback()

    def draw(self, screen):
        """Отрисовывает окно загрузки."""
        draw_gradient(screen, (100, 140, 210), (200, 230, 255)) # Gradient

        # Отрисовка списка файлов
        y_offset = 50
        for i, (button_rect, file) in enumerate(self.file_buttons):
            color = (100, 100, 100) if file != self.selected_file else (150, 150, 150)
            pygame.draw.rect(screen, color, button_rect)
            text_surface = self.font.render(file, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        # Отрисовка кнопок "Загрузить", "Удалить", "Закрыть"
        load_button_clicked = create_button(screen, self.load_button_rect.x, self.load_button_rect.y,
                                           self.load_button_rect.width, self.load_button_rect.height,
                                           "Загрузить", (0, 128, 255), (0, 80, 200), self.font, (255, 255, 255))
        delete_button_clicked = create_button(screen, self.delete_button_rect.x, self.delete_button_rect.y,
                                           self.delete_button_rect.width, self.delete_button_rect.height,
                                           "Удалить", (255, 50, 50), (200, 0, 0), self.font, (255, 255, 255))
        close_button_clicked = create_button(screen, self.close_button_rect.x, self.close_button_rect.y,
                                           self.close_button_rect.width, self.close_button_rect.height,
                                           "Закрыть", (100, 100, 100), (80, 80, 80), self.font, (255, 255, 255))

    def load_selected_game(self):
        """Загружает выбранный файл сохранения."""
        if self.selected_file:
            file_path = os.path.join(self.save_dir, self.selected_file)
            try:
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                    self.load_callback(data)  # Вызываем функцию загрузки из main.py
                self.running = False
                self.close_callback() # Закрываем окно загрузки
            except FileNotFoundError:
                print(f"Файл не найден: {file_path}")
            except pickle.PickleError:
                print(f"Ошибка при загрузке файла: {file_path}")

    def delete_selected_game(self):
        """Удаляет выбранный файл сохранения."""
        if self.selected_file:
            file_path = os.path.join(self.save_dir, self.selected_file)
            try:
                os.remove(file_path)
                print(f"Файл удален: {file_path}")
                # Обновляем список файлов
                self.file_list = get_saved_games(self.save_dir)
                self.create_file_buttons() # Recreate buttons
                self.selected_file = None # Clear selection
            except FileNotFoundError:
                print(f"Файл не найден: {file_path}")