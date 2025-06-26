import pygame

class WinAnimation:
    def __init__(self, screen, board, font, grid_pos, cell_size):
        self.screen = screen
        self.board = board
        self.font = font
        self.grid_pos = grid_pos
        self.cell_size = cell_size
        self.colors = [(0, 255, 0)] * 81  # Зеленый для всех ячеек
        self.winner_text = font.render("Winner!", True, (255, 255, 255))
        self.winner_rect = self.winner_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        self.animation_duration = 2000  # 2 секунды
        self.start_time = pygame.time.get_ticks()

    def draw(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time < self.animation_duration:
            # Анимация (пока просто отображаем зеленые цифры)
            self.draw_green_numbers()
            self.screen.blit(self.winner_text, self.winner_rect)
        else:
            return True  # Анимация завершена

        return False  # Анимация еще не завершена

    def draw_green_numbers(self):
        for i in range(9):
            for j in range(9):
                number = self.board[i][j]
                if number != 0:
                    text_surface = self.font.render(str(number), True, (0, 255, 0))
                    # Используем grid_pos для смещения текста на доску
                    text_rect = text_surface.get_rect(center=(self.grid_pos[0] + j * self.cell_size + self.cell_size // 2,
                                                               self.grid_pos[1] + i * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text_surface, text_rect)