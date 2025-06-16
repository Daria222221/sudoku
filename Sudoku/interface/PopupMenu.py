import pygame
from major.constants import *

class PopupMenu:
    def __init__(self, x, y, width, height, options):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.option_height = height // len(options)  # Высота каждой опции
        self.selected_option = None
        self.visible = False
        self.hovered_option = None  # Индекс опции, на которую наведен курсор

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.visible:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                option_index = (mouse_pos[1] - self.rect.top) // self.option_height
                if 0 <= option_index < len(self.options):
                    self.selected_option = self.options[option_index]
                    self.visible = False  # Закрываем меню после выбора

        # Обработка движения мыши
        if event.type == pygame.MOUSEMOTION and self.visible:
            mouse_pos = event.pos
            if self.rect.collidepoint(mouse_pos):
                option_index = (mouse_pos[1] - self.rect.top) // self.option_height
                if 0 <= option_index < len(self.options):
                    self.hovered_option = option_index
                else:
                    self.hovered_option = None
            else:
                self.hovered_option = None

    def draw(self, screen, font):
        if self.visible:
            pygame.draw.rect(screen, (200, 220, 255), self.rect)  # Фон меню
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + i * self.option_height,
                                          self.rect.width, self.option_height)
                # Подсветка при наведении
                if i == self.hovered_option:
                    pygame.draw.rect(screen, (160, 180, 215), option_rect)
                #Рамка если не наведена
                else:
                    pygame.draw.rect(screen, (180, 200, 235), option_rect, 1)  # Рамка опции

                text_surface = font.render(option, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=option_rect.center)
                screen.blit(text_surface, text_rect)