import pygame
from database.Database import db_conn
pygame.init()

if __name__ == "__main__":
    from game_options.Game import Game
    player = db_conn.create_player("Kirill")
    game_id = db_conn.add_game_session(player)
    if game_id is not None:
        game = Game(game_id=game_id, player=player)
        game.run_game()
    else:
        print("Пользователя нет")
