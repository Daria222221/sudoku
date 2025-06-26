import pygame

class ExitButton:
    def __init__(self, x, y, size, normal_color, hover_color):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.normal_color
        pygame.draw.line(screen, color,
                         (self.x, self.y),
                         (self.x + self.size, self.y + self.size), 2)
        pygame.draw.line(screen, color,
                         (self.x + self.size, self.y),
                         (self.x, self.y + self.size), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True  # Возвращаем True при клике
        return False
