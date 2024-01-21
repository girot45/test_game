DATABASE_LOCATION = "leaderboard.db"

DATABASE_CREATE_TABLES = '''CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reg_date TEXT NOT NULL,
                best_scores INTEGER NOT NULL DEFAULT 0 
            );
               
            CREATE TABLE IF NOT EXISTS game_session (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_start VARCHAR,
                player_id INTEGER,
                scores INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES players(id)
            );
            
            CREATE TABLE IF NOT EXISTS game_session_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                event_description TEXT NOT NULL,
                event_status TEXT NOT NULL,
                datetime VARCHAR,
                FOREIGN KEY (game_id) REFERENCES game_session(id)
            );'''
