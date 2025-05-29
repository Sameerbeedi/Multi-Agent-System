# memory/memory_store.py
import sqlite3
import datetime

class MemoryStore:
    def __init__(self, db_file='memory.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, type TEXT, intent TEXT,
            extracted TEXT, timestamp TEXT
        )
        ''')

    def log(self, source, filetype, intent, extracted):
        self.conn.execute('''
        INSERT INTO memory (source, type, intent, extracted, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''', (source, filetype, intent, str(extracted), datetime.datetime.now().isoformat()))
        self.conn.commit()
