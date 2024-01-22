import sys
import time
from random import randint

import pygame

from database.Player import Player
from database.utils import create_liderboard
from game_options.Font import font_count, font_game_over, font_player, \
    font_leaderboard
from game_options.game_options import COLUMNS, ROWS, FONT_SIZE, PADDING, \
    RECT_COLOR_0, RECT_COLOR_1, SIZE_RECT, HEADER_RECT, FRAME_COLOR, \
    FOOD_COLOR, CAPTION, FPS, FRAME_GAME_OVER
from game_options.Snake import Snake
from game_options.Rect import Rect

from database.Database import db_conn


class Game:
    def __init__(
            self,
            player: Player,
            columns: int = COLUMNS,
            rows: int = ROWS,
            font_size: int = FONT_SIZE,
            padding: int = PADDING,
            fps: int = FPS,

    ):
        self.player = player
        self.game_over = False
        self.columns = columns
        self.rows = rows
        self.padding = padding
        self.width = SIZE_RECT * (self.columns + 2) + self.padding * self.columns
        self.height = SIZE_RECT * (self.rows + 2) + self.padding * self.rows + HEADER_RECT

        self.snake = Snake(self.columns // 2, self.rows // 2)

        self.font = pygame.font.SysFont('', font_size)
        self.odd_color = RECT_COLOR_1
        self.even_color = RECT_COLOR_0
        self.mode = "game"
        self.screen = pygame.display.set_mode(
            (
                self.width,
                self.height
            )
        )
        self.fps = fps
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(CAPTION)


    def set_screen_params(self, font, color=FRAME_COLOR):
        self.screen.fill(color)
        self.screen.blit(font.text, font.text_rect)

    def generate_random_food(self):
        x = randint(0, self.columns - 1)
        y = randint(0, self.rows - 1)
        food = Rect(x, y)
        while food in self.snake.parts:
            x = randint(0, self.columns - 1)
            y = randint(0, self.rows - 1)
            food = Rect(x, y)
        return food

    def draw_food(self, food):
        food.draw_rect(
            FOOD_COLOR,
            self.screen,
            HEADER_RECT
        )

    def draw_map(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if (row + column) % 2 == 0:
                    color = self.even_color
                else:
                    color = self.odd_color
                rect = Rect(column, row)
                rect.draw_rect(color, self.screen, HEADER_RECT)

    def check_is_win(self):
        return len(self.snake.parts) == self.rows * self.columns

    def check_inside(self, rect):
        return 0 <= rect.x <= self.columns - 1 and 0 <= rect.y <= self.rows - 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                self.mode = "win" if self.mode == "win" else "end"

            elif event.type == pygame.KEYDOWN:
                if ((event.key in [pygame.K_UP, pygame.K_w]) and
                        self.snake.speed != [0, 1]):
                    self.snake.set_speed([0, -1])
                elif ((event.key in [pygame.K_DOWN, pygame.K_s]) and
                      self.snake.speed != [0, -1]):
                    self.snake.set_speed([0, 1])
                elif ((event.key in [pygame.K_RIGHT, pygame.K_d]) and
                      self.snake.speed != [-1, 0]):
                    self.snake.set_speed([1, 0])
                elif ((event.key in [pygame.K_LEFT, pygame.K_a]) and
                      self.snake.speed != [1, 0]):
                    self.snake.set_speed([-1, 0])
            db_conn.update_player_scores(self.player.id, self.player.best_scores)

    def show_leaderboard(self):
        leaderboard = create_liderboard(db_conn.get_players())
        for i, row in enumerate(leaderboard):
            font_leaderboard.render(row)
            font_leaderboard.set_rect(
                center=(self.width // 2, 120 + 40 * (i + 1)))
            self.screen.blit(font_leaderboard.text,
                             font_leaderboard.text_rect)

    def run_game(self):
        db_conn.add_game_session_log(
            "Начало игры",
            "info"
        )
        food = self.generate_random_food()
        font_player.set_rect(topleft=(20, 60))
        font_player.render(f"Игрок: {self.player.name}")
        self.set_screen_params(font_count)
        self.screen.blit(font_player.text, font_player.text_rect)
        self.draw_map()
        self.draw_food(food)
        self.snake.draw(self.screen)
        pygame.display.flip()
        time.sleep(2)
        count = 0

        while not self.game_over:
            self.handle_events()
            if self.mode == "end":
                font_game_over.set_rect(
                    center=(self.width // 2, 50)
                )
                self.set_screen_params(
                    font_game_over,
                    FRAME_GAME_OVER
                )
                font_count.set_rect(
                    center=(self.width // 2, 50 + 60)
                )
                self.screen.blit(
                    font_count.text,
                    font_count.text_rect
                )
                self.show_leaderboard()

            elif self.mode == "win":
                font_count.render(f'Победа! Ваш счет: {count}')
                font_count.set_rect(center=(self.width // 2, 50))
                self.set_screen_params(font_count, FRAME_COLOR)
                self.show_leaderboard()
            else:
                new_head = self.snake.head + self.snake.speed
                if (not self.check_inside(new_head) or
                        self.snake.check_collision(new_head)):
                    self.mode = "end"
                    continue
                self.snake.add_part(new_head)

                if food == self.snake.head:
                    count += 1
                    if count >= self.player.best_scores:
                        self.player.best_scores = count
                    font_count.render(f"Счет: {count}")
                    food = self.generate_random_food()
                    if count % 10 == 0:
                        self.fps += 1

                    if self.check_is_win():
                        self.mode = "win"
                        continue
                else:
                    self.snake.parts.pop(0)

                self.set_screen_params(font_count)

                self.screen.blit(font_player.text, font_player.text_rect)
                self.draw_map()
                self.snake.draw(self.screen)
                self.draw_food(food)
            self.clock.tick(self.fps)
            pygame.display.flip()
        print(self.player.best_scores)
        db_conn.add_game_session_log(
            "Конец игры",
            "info"
        )

        return self.player


