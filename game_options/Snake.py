from game_options.Rect import Rect
from game_options.game_options import HEADER_RECT, COLOR_SNAKE


class Snake:
    def __init__(self, x, y):
        self.color = COLOR_SNAKE
        self.parts = [Rect(x, y)]
        self.head = self.parts[-1]
        self.speed = [0, 1]

    def set_speed(self, speed):
        self.speed = speed

    def add_part(self, rect):
        self.parts.append(rect)
        self.head = self.parts[-1]
        return self.head

    def check_collision(self, new_head: Rect):
        return new_head in self.parts

    def draw(self, screen):
        for part in self.parts:
            part.draw_rect(self.color, screen, HEADER_RECT)
