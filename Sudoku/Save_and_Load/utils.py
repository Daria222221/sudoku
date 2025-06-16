import os
import pygame

def get_saved_games(save_dir):
    """Возвращает список файлов сохранений в указанной директории."""
    try:
        return [f for f in os.listdir(save_dir) if f.endswith(".sudoku")]
    except FileNotFoundError:
        print(f"Директория сохранений не найдена: {save_dir}")
        return []

def create_button(screen, x, y, width, height, text, color, hover_color, font, text_color, action=None):
    """Создает прямоугольную кнопку с текстом."""
    button_rect = pygame.Rect(x, y, width, height)
    mouse_pos = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint(mouse_pos)
    current_color = hover_color if hovered else color

    pygame.draw.rect(screen, current_color, button_rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    if hovered and pygame.mouse.get_pressed()[0] and action is not None:
        action()  # Выполняем действие при клике
        return True
    return False