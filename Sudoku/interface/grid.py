import pygame

from major.constants import *


def draw_grid(surface, x, y, size, mouse_pos=None, selected_cell=None):
    cell_size = size // 9
    corner_radius = 16

    # 1. Основное поле с прозрачным центром
    field_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(field_surf, (*DARK_BLUE, 255),
                     (0, 0, size, size),
                     width=3,
                     border_radius=corner_radius)

    # 2. Сетка на отдельной поверхности
    grid_surf = pygame.Surface((size - 6, size - 6), pygame.SRCALPHA)
    grid_surf.fill((0, 0, 0, 0))

    # Вертикальные линии
    for i in range(1, 9):
        line_x = i * cell_size - 3
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(grid_surf, (*DARK_BLUE, 255),
                         (line_x, 0),
                         (line_x, size - 6),
                         width)

    # Горизонтальные линии
    for i in range(1, 9):
        line_y = i * cell_size - 3
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(grid_surf, (*DARK_BLUE, 255),
                         (0, line_y),
                         (size - 6, line_y),
                         width)

    field_surf.blit(grid_surf, (3, 3))
    surface.blit(field_surf, (x, y))

    # 3. Подсветка при наведении (все клетки, включая угловые)
    if mouse_pos:
        mx, my = mouse_pos
        grid_x = mx - x
        grid_y = my - y

        if 0 <= grid_x < size and 0 <= grid_y < size:
            col = min(max(0, int(grid_x / cell_size)), 8)
            row = min(max(0, int(grid_y / cell_size)), 8)

            # Создаем поверхность для подсветки
            highlight = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            highlight.fill((*HIGHLIGHT, 100))  # Полупрозрачная подсветка

            # Для угловых клеток применяем маску
            if (row, col) in [(0, 0), (0, 8), (8, 0), (8, 8)]:
                mask = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                if (row, col) == (0, 0):
                    pygame.draw.rect(mask, (255, 255, 255, 255),
                                     (0, 0, cell_size, cell_size),
                                     border_top_left_radius=corner_radius)
                elif (row, col) == (0, 8):
                    pygame.draw.rect(mask, (255, 255, 255, 255),
                                     (0, 0, cell_size, cell_size),
                                     border_top_right_radius=corner_radius)
                elif (row, col) == (8, 0):
                    pygame.draw.rect(mask, (255, 255, 255, 255),
                                     (0, 0, cell_size, cell_size),
                                     border_bottom_left_radius=corner_radius)
                else:
                    pygame.draw.rect(mask, (255, 255, 255, 255),
                                     (0, 0, cell_size, cell_size),
                                     border_bottom_right_radius=corner_radius)

                highlight.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            surface.blit(highlight, (x + col * cell_size, y + row * cell_size))

    # 4. Выделение выбранной клетки (темно-синее)
    if selected_cell:
        row, col = selected_cell
        selection = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        selection.fill((*DARK_BLUE, 150))  # Полупрозрачный темно-синий

        if (row, col) in [(0, 0), (0, 8), (8, 0), (8, 8)]:
            mask = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            if (row, col) == (0, 0):
                pygame.draw.rect(mask, (255, 255, 255, 255),
                                 (0, 0, cell_size, cell_size),
                                 border_top_left_radius=corner_radius)
            elif (row, col) == (0, 8):
                pygame.draw.rect(mask, (255, 255, 255, 255),
                                 (0, 0, cell_size, cell_size),
                                 border_top_right_radius=corner_radius)
            elif (row, col) == (8, 0):
                pygame.draw.rect(mask, (255, 255, 255, 255),
                                 (0, 0, cell_size, cell_size),
                                 border_bottom_left_radius=corner_radius)
            else:
                pygame.draw.rect(mask, (255, 255, 255, 255),
                                 (0, 0, cell_size, cell_size),
                                 border_bottom_right_radius=corner_radius)

            selection.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        surface.blit(selection, (x + col * cell_size, y + row * cell_size))


# def draw_numbers(surface, board, x, y, size, font):
#     cell_size = size // 9
#     for row in range(9):
#         for col in range(9):
#             value = board.get_cell(row, col)
#             if value != 0:
#                 color = DARK_BLUE if board.original[row][col] != 0 else (50, 120, 200)
#                 num_surf = font.render(str(value), True, color)
#                 num_rect = num_surf.get_rect(center=(
#                     x + col * cell_size + cell_size // 2,
#                     y + row * cell_size + cell_size // 2
#                 ))
#                 surface.blit(num_surf, num_rect)


# def draw_numbers(surface, board, x, y, size, font):
#     cell_size = size // 9
#
#     for row in range(9):
#         for col in range(9):
#             value = board.get_cell(row, col)
#             if value != 0:
#                 # Цвета: исходные - темно-синие, введенные - синие
#                 color = DARK_BLUE2 if board.original[row][col] != 0 else (30, 60, 90)
#                 num_surf = font.render(str(value), True, color)
#
#                 # Позиционирование с учетом угловых клеток
#                 pos_x = x + col * cell_size + cell_size // 2 - num_surf.get_width() // 2
#                 pos_y = y + row * cell_size + cell_size // 2 - num_surf.get_height() // 2
#
#                 # Для угловых клеток делаем небольшой отступ от края
#                 if (row, col) == (0, 0):
#                     pos_x += 3
#                     pos_y += 3
#                 elif (row, col) == (0, 8):
#                     pos_x -= 3
#                     pos_y += 3
#                 elif (row, col) == (8, 0):
#                     pos_x += 3
#                     pos_y -= 3
#                 elif (row, col) == (8, 8):
#                     pos_x -= 3
#                     pos_y -= 3
#
#                 surface.blit(num_surf, (pos_x, pos_y))
def draw_numbers(surface, board, x, y, size, font, selected_cell=None):
    cell_size = size // 9

    for row in range(9):
        for col in range(9):
            value = board.get_cell(row, col)
            if value != 0:
                # Определяем, является ли цифра частью изначальной доски
                if board.original[row][col] != 0:
                    color = (255, 255, 255)  # Белый для изначальных цифр
                else:
                    color = DARK_BLUE  # Другой цвет для введенных цифр (был DARK_BLUE, можно изменить)

                # Если клетка выбрана, то цифра белая, переопределяем цвет
                if selected_cell and (row, col) == selected_cell:
                    color = (255, 255, 255) # Белый цвет

                num_surf = font.render(str(value), True, color)
                num_rect = num_surf.get_rect(center=(x + col * cell_size + cell_size // 2,
                                                      y + row * cell_size + cell_size // 2))

                surface.blit(num_surf, num_rect)


def get_clicked_cell(pos):
    """Возвращает (row, col) если клик был по сетке, иначе None"""
    x, y = pos
    grid_x = x - GRID_POS[0]
    grid_y = y - GRID_POS[1]

    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        col = grid_x // CELL_SIZE
        row = grid_y // CELL_SIZE
        return row, col
    return None