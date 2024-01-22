import sys
import threading
import tkinter as tk
from tkinter import ttk
import pygame

from database.Database import db_conn
from menu.utils import create_options_list


class GameWindow:
    def __init__(self):
        self.pygame_thread = None
        self.root = tk.Tk()
        self.root.title("Игра")
        self.root.geometry("400x300")

        # Кнопка "Начать игру"
        start_game_button = tk.Button(
            self.root,
            text="Начать игру",
            command=self.enter_nickname,
            width=20,
            height=2
        )
        start_game_button.pack(pady=10)

        # Кнопка "Правила"
        rules_button = tk.Button(
            self.root,
            text="Правила",
            command=self.show_rules,
            width=20,
            height=2
        )
        rules_button.pack(pady=10)

        # Кнопка "Топ игроков"
        top_players_button = tk.Button(
            self.root,
            text="Топ игроков",
            command=self.show_top_players,
            width=20,
            height=2
        )
        top_players_button.pack(pady=10)

        # Флаг для завершения цикла игры
        self.game_over_flag = False

    def enter_nickname(self):
        input_window = tk.Toplevel(self.root)
        input_window.title("Введите данные")
        input_window.geometry("500x300")

        res = db_conn.get_players(limit=None)
        options = create_options_list(res)
        selected_option = tk.StringVar()
        label = tk.Label(input_window,
                         text="Выберите свой ник или введите из списка",
                         font=("Arial", 12))
        label.pack(pady=10)
        dropdown = ttk.Combobox(input_window,
                                textvariable=selected_option,
                                values=options)
        dropdown.set("")
        dropdown.pack(pady=10)

        start_button = tk.Button(input_window,
                                 text="Начать игру",
                                 command=lambda: self.start_game(selected_option.get(), input_window),
                                 width=15,
                                 height=2)
        start_button.pack(pady=10)

    def start_game(self, selected_option, input_window):
        input_window.destroy()
        if selected_option.replace(" ", "") != "":
            pygame.init()
            self.pygame_thread = threading.Thread(
                target=self.run_pygame,
                args=(selected_option.strip(),)
            )
            self.pygame_thread.start()

    def run_pygame(self, selected_option):
        from game_options.Game import Game
        player = db_conn.create_player(selected_option)
        if player is not None:
            game = Game(player=player)
            player = game.run_game()
        else:
            print("Пользователя нет")
        db_conn.update_player_scores(
            player_id=player.id,
            score=player.best_scores
        )
        pygame.quit()
        self.root.quit()
        sys.exit()


    def stop_game(self):
        if self.pygame_thread and self.pygame_thread.is_alive():
            self.pygame_thread.join()

    def show_rules(self):
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила")

        rules_text = "Правила змейки:\n\n1. Управление стрелками на клавиатуре.\n2. Собирайте еду и растите, избегайте столкновений со стенами и самим собой."
        rules_label = tk.Label(rules_window, text=rules_text, padx=20,
                               pady=20)
        rules_label.pack()

        close_button = tk.Button(rules_window, text="Закрыть",
                                 command=rules_window.destroy)
        close_button.pack(pady=10)

    def show_top_players(self):
        top_players_window = tk.Toplevel(self.root)
        top_players_window.title("Топ игроков")
        res = db_conn.get_players()
        top_players = []
        for player in res:
            top_players.append(
                (player[1], player[3])
            )

        # Создаем Treeview для отображения таблицы
        tree = ttk.Treeview(top_players_window, columns=("Имя", "Лучший счет"), show="headings")

        # Заголовки колонок
        tree.heading("Имя", text="Имя")
        tree.heading("Лучший счет", text="Лучший счет")

        # Заполняем таблицу данными (ваша логика получения топа игроков)
        # Пример данных

        for player in top_players:
            tree.insert("", "end", values=player)

        # Упаковываем Treeview
        tree.pack(pady=20)

        close_button = tk.Button(top_players_window, text="Закрыть", command=top_players_window.destroy)
        close_button.pack(pady=10)

    def run(self):
        self.root.mainloop()


def run_game_window():
    game_window = GameWindow()
    game_window.run()