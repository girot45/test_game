import os
from datetime import datetime
from sqlite3 import connect, Cursor
from typing import Optional

from database.database_settings import DATABASE_LOCATION, \
    DATABASE_CREATE_TABLES
from database.Player import Player


class Database:
    def __init__(self):
        self.connection = connect(DATABASE_LOCATION, check_same_thread=False)
        self.create_tables()

    def get_cursor(self) -> Cursor:
        return self.connection.cursor()

    def close_connection(self):

        self.connection.close()

    def create_tables(self):
        cursor = self.get_cursor()
        try:
            if not os.path.exists(DATABASE_LOCATION):
                with open(DATABASE_LOCATION, 'w'):
                    pass
            try:
                cursor.execute("SELECT * FROM players")
            except:
                for statement in DATABASE_CREATE_TABLES.split(';'):
                    cursor.execute(statement)
                self.connection.commit()
                self.add_game_session_log(
                    "Таблицы созданы",
                    "info"
                )
            finally:
                cursor.close()
        except Exception as e:
            print(e)
            self.add_game_session_log(
                f"{e}",
                "error"
            )
            self.connection.rollback()
        finally:
            cursor.close()

    def check_player(self, player_name: str):
        try:
            player = self.get_player(player_name=player_name)
            if player:
                return True, player
            else:
                return False, None
        except Exception as e:
            self.add_game_session_log(
                f"{e}",
                "error"
            )
            return False, None

    def create_player(self, name: str):
        cursor = self.get_cursor()
        try:
            self.add_game_session_log(
                f"Новый игрок {name}",
                "info"
            )
            is_in_db, player = self.check_player(player_name=name)
            if not is_in_db:
                sql = "INSERT INTO players (name, reg_date) values ($1, $2)"
                cursor.execute(sql, [name,
                                     datetime.now().date().strftime(
                                         "%Y-%m-%d")])
                self.connection.commit()
                player_id = cursor.lastrowid
                player = Player(
                    name=name,
                    player_id=player_id,
                    best_scores=0
                )
                cursor.close()
            return player

        except Exception as e:
            self.add_game_session_log(
                f"{e}",
                "error"
            )
            self.connection.rollback()
        finally:
            cursor.close()

    def get_player(self, player_name: str, limit: int = 1) -> Optional[Player]:
        cursor = self.get_cursor()
        try:
            sql = "SELECT * FROM players WHERE name = $1 LIMIT $2"
            cursor.execute(sql, [player_name, limit])
            result = cursor.fetchone()

            if result:
                return Player(
                    player_id=result[0],
                    name=result[1],
                    best_scores=result[3]
                )
            else:
                return None
        except Exception as e:
            self.add_game_session_log(
                f"{e}",
                "error"
            )
            return None
        finally:
            cursor.close()

    def get_players(self, limit: Optional[int] = 5):
        cursor = self.get_cursor()
        try:
            sql = "SELECT * FROM players ORDER BY best_scores DESC"
            if limit is not None:
                sql += " LIMIT $s"
                cursor.execute(sql, [limit])
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(e)
            self.add_game_session_log(
                f"{e}",
                "error"
            )
        finally:
            cursor.close()

    def add_game_session_log(
            self,
            event_description: str,
            event_status: str
    ):
        cursor = self.get_cursor()
        try:
            sql = ("INSERT INTO logs (event_description, event_status, "
                   "datetime) VALUES ($1, $2, $3)")
            cursor.execute(
                sql,
                [
                    event_description,
                    event_status,
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ]
            )
            self.connection.commit()
        except:
            # Общая обработка других исключений
            self.connection.rollback()
        finally:
            cursor.close()

    def update_player_scores(self, player_id: int, score: int) -> None:
        cursor = self.get_cursor()
        try:
            self.add_game_session_log(
                f"Новый рекорд игрока {player_id}",
                "info"
            )
            sql = "UPDATE players SET best_scores=$1 WHERE id=$2"
            cursor.execute(sql, [score, player_id])
            self.connection.commit()
        except Exception as e:
            self.add_game_session_log(
                f"{e}",
                "error"
            )
            self.connection.rollback()


db_conn = Database()
