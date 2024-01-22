DATABASE_LOCATION = "leaderboard.db"

DATABASE_CREATE_TABLES = '''CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reg_date TEXT NOT NULL,
                best_scores INTEGER NOT NULL DEFAULT 0 
            );
            
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_description TEXT NOT NULL,
                event_status TEXT NOT NULL,
                datetime VARCHAR
            );
            INSERT INTO players (name, reg_date, best_scores) 
            VALUES ('John', '2020-01-01', 0);
            INSERT INTO players (name, reg_date, best_scores) 
            VALUES ('Jane', '2020-01-02', 5);
            INSERT INTO players (name, reg_date, best_scores) 
            VALUES ('Alice', '2020-01-03', 14);
            INSERT INTO players (name, reg_date, best_scores) 
            VALUES ('Martin', '2020-01-04', 43)
            '''
