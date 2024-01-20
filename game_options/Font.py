import pygame
from game_options.game_options import FONT_SIZE


class FontsParametrs:
    def __init__(
            self,
            text: str,
            color: tuple,
            antialias: bool = True,
            size: int = FONT_SIZE,
            **kwargs
    ):
        self.color = color
        self.antialias = antialias
        self.font = pygame.font.SysFont(None, size)
        self.text = self.render(text)
        self.text_rect = self.set_rect(**kwargs)

    def render(self, text):
        self.text = self.font.render(text, self.antialias, self.color)
        return self.text

    def set_rect(self, **kwargs):
        self.text_rect = self.text.get_rect(**kwargs)
        return self.text_rect


font_count = FontsParametrs(
    size=60,
    text='Счет: 0',
    antialias=True,
    color=(255, 255, 255),
    topleft=(20, 20)
)

font_game_over = FontsParametrs(
    size=60,
    text='GAME OVER',
    antialias=True,
    color=(255, 255, 255),
    topleft=(20, 20)
)
