from datetime import datetime
from sqlite3 import connect, Cursor
from typing import Optional

from database.database_settings import DATABASE_LOCATION, \
    DATABASE_CREATE_TABLES
from database.Player import Player


class Database:
    def __init__(self):
        self.connection = connect(DATABASE_LOCATION)
        self.create_tables()

    def get_cursor(self) -> Cursor:
        return self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create_tables(self):
        try:
            cursor = self.get_cursor()
            cursor.execute(DATABASE_CREATE_TABLES)
            self.connection.commit()
        except Exception as e:
            print(f"Произошла ошибка при создании таблиц: {e}")
            self.connection.rollback()

    def check_player(self, player_name: str) -> bool:
        try:
            if self.get_player(player_name=player_name):
                return True
            else:
                return False
        except Exception as e:
            print(f"Произошла ошибка при поиске: {e}")
            return False

    def create_player(self, name: str):
        try:
            cursor = self.get_cursor()
            self.check_player(player_name=name)
            if not cursor.rowcount:
                sql = "INSERT INTO players (name, reg_date) values ($1, $2)"
                cursor.execute(sql, [name,
                                     datetime.now().date().strftime(
                                         "%Y-%m-%d")])
                self.connection.commit()
        except Exception as e:
            print(f"Произошла ошибка при добавлении игрока: {e}")
            self.connection.rollback()

    def get_player(self, player_name: str, limit: int = 1) -> Optional[Player]:
        try:
            cursor = self.get_cursor()
            sql = "SELECT * FROM players WHERE name = $1 LIMIT $2"
            cursor.execute(sql, [player_name, limit])
            result = cursor.fetchone()
            if cursor.rowcount:
                return Player(
                    player_id=result[0],
                    name=result[1],
                    best_scores=result[3]
                )
            else:
                return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    def add_game_session(self, player: Player):
        try:
            cursor = self.get_cursor()
            sql = "INSERT INTO game_session (time_start, player_id) VALUES ($1, $2)"
            cursor.execute(
                sql,
                [
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    player.id
                ]
            )
            self.connection.commit()
            game_id = cursor.lastrowid
            return game_id
        except Exception as e:
            print(f"Произошла ошибка при создании сессии: {e}")
            self.connection.rollback()

    def update_game_session(self, game_id: int, scores: int):
        try:
            with self.get_cursor() as cursor:
                sql = "UPDATE game_session SET scores = $1 WHERE id = $2"
                cursor.execute(
                    sql,
                    [
                        scores,
                        game_id
                    ]
                )
                self.connection.commit()
        except Exception as e:
            print(f"Error updating game session: {e}")
            self.connection.rollback()


    def get_top_five_players(self, limit: int = 5):
        try:
            cursor = self.get_cursor()
            sql = "SELECT * FROM players LIMIT $s"
            cursor.execute(sql, [limit])
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Произошла ошибка при получении топа игроков: {e}")

    def add_game_session_log(
            self,
            game_id: int,
            event_description: str,
            event_status: str
    ):
        try:
            with self.get_cursor() as cursor:
                sql = ("INSERT INTO game_session_logs (game_id, event_description, event_status) "
                       "VALUES ($1, $2, $3)")
                cursor.execute(
                    sql,
                    [
                        game_id,
                        event_description,
                        event_status
                    ]
                )
                self.connection.commit()
        except Exception as e:
            # Общая обработка других исключений
            print(f"Произошла ошибка при добавлении лога: {e}")
            self.connection.rollback()


db_conn = Database()
print(db_conn.get_player("Kirill"))