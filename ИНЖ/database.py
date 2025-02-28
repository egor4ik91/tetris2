import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('tetris_scores.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def save_score(self, username, score):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))
        self.conn.commit()

    def get_top_scores(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT username, score FROM scores ORDER BY score DESC LIMIT 5')
        return cursor.fetchall()

    def __del__(self):
        self.conn.close()