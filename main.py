import pygame
pygame.init()

if __name__ == "__main__":
    from menu.window import GameWindow
    from database.Database import db_conn
    db_conn.add_game_session_log(
        "Запущена игра",
        "info"
    )
    game_window = GameWindow()
    game_window.run()
