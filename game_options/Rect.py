import pygame

from game_options.game_options import PADDING, SIZE_RECT


class Rect:
    def __init__(self, x, y, size=SIZE_RECT, padding=PADDING):
        # Номер клетки по ширине
        self.x = x
        # Номер клетки по высоте
        self.y = y
        self.size = size
        self.padding = padding

    def __eq__(self, other):
        return (isinstance(other, Rect) and
                self.x == other.x and self.y == other.y)

    def __add__(self, other):
        return Rect(self.x + other[0], self.y + other[1])

    def draw_rect(self, color, screen, HEADER_RECT):
        """Функция отрисовки одной клетки"""
        pygame.draw.rect(
            screen,
            color,
            [
                self.size + self.x * self.size + self.padding * (self.x + 1),
                HEADER_RECT + self.size + self.y * self.size + self.padding * (self.y + 1),
                self.size,
                self.size
            ]
        )