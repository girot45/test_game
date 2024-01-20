import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("leaderboard.db")
        self.cursor = self.connection.cursor()

        # Создание таблицы, если её нет
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS leaderboard (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  player_name TEXT,
                  score INTEGER);
               
               CREATE TABLE IF NOT EXISTS game_session (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  time_start VARCHAR
               )                ''')
        self.connection.commit()

    def add_score(self, player_name, score):
        self.cursor.execute("INSERT INTO leaderboard (player_name, score) VALUES (?, ?)", (player_name, score))
        self.connection.commit()

    def get_leaderboard(self):
        self.cursor.execute("SELECT player_name, score FROM leaderboard ORDER BY score DESC LIMIT 5")
        return self.cursor.fetchall()
