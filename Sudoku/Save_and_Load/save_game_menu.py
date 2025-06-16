import pygame
from major.constants import *
from Save_and_Load.utils import create_button
from interface.theme import draw_gradient  # !!! ДОБАВЬ ЭТУ СТРОКУ !!!

class SaveGameMenu:
    def __init__(self, screen, root_dir, save_callback, close_callback):
        self.screen = screen
        self.root_dir = root_dir
        self.save_callback = save_callback  # Функция сохранения
        self.close_callback = close_callback  # Функция закрытия меню
        self.font = pygame.font.SysFont(None, 32)
        self.running = True
        self.input_box = pygame.Rect(WIDTH // 2 - 100, 200, 200, 32)
        self.color_inactive = pygame.Color(10, 13, 99)
        self.color_active = pygame.Color(0, 26, 255)
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.save_button_rect = pygame.Rect(WIDTH // 2 - 75, 300, 150, 50)
        self.cancel_button_rect = pygame.Rect(WIDTH // 2 - 75, 370, 150, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive

            # Обработка кнопок "Сохранить" и "Отмена"
            if self.save_button_rect.collidepoint(event.pos):
                self.save_callback(self.text)  # Вызываем функцию сохранения
                self.close_callback()
            if self.cancel_button_rect.collidepoint(event.pos):
                self.close_callback()


        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.save_callback(self.text)
                    self.close_callback()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        pass

    def draw(self, screen):
        # Рисуем градиентный фон
        draw_gradient(screen, (100, 140, 210), (200, 230, 255)) # Gradient
        # Рисуем поле ввода
        pygame.draw.rect(screen, self.color, self.input_box, 2)

        # Рисуем текст
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Пересчитываем размер поля ввода
        self.input_box.w = max(200, text_surface.get_width() + 10)

        # Рисуем кнопки "Сохранить" и "Отмена"
        create_button(screen, self.save_button_rect.x, self.save_button_rect.y,
                      self.save_button_rect.width, self.save_button_rect.height,
                      "Сохранить", (0, 128, 255), (0, 80, 200), self.font, (255, 255, 255))
        create_button(screen, self.cancel_button_rect.x, self.cancel_button_rect.y,
                      self.cancel_button_rect.width, self.cancel_button_rect.height,
                      "Отмена", (100, 100, 100), (80, 80, 80), self.font, (255, 255, 255))